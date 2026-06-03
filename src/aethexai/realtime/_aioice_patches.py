"""Compatibility patches for aioice's TURN client (RFC 5766 relay behavior).

Fixes:
- Register missing DATA attribute (0x0013) in STUN
- Add CreatePermission (RFC 5766 Section 9) -- aioice never sends it
- Patch send_data to fall back to Send indication when ChannelBind 401 fails
- Handle Data indications for relayed peer data

Guard with _patched flag so patches only apply once.
"""

from __future__ import annotations

import asyncio
import logging
import struct
import time
import warnings

logger = logging.getLogger(__name__)

_TESTED_AIOICE_VERSION = "0.9.0"


def apply_patches() -> None:
    """Apply aioice TURN compatibility patches.

    Safe to call multiple times -- patches are applied at most once.
    """
    try:
        from aioice import stun, turn
    except ImportError:
        raise ImportError(
            "aioice is required for WebRTC support. Install it with: pip install aethexai[realtime]"
        )

    try:
        import importlib.metadata

        aioice_version = importlib.metadata.version("aioice")
        if aioice_version != _TESTED_AIOICE_VERSION:
            warnings.warn(
                f"aioice {aioice_version} detected; patches were tested against "
                f"{_TESTED_AIOICE_VERSION}. TURN relay may not work correctly.",
                stacklevel=2,
            )
    except Exception:
        pass

    cls = turn.TurnClientMixin
    if getattr(cls, "_patched", False):
        return

    if 0x0013 not in stun.ATTRIBUTES_BY_TYPE:
        data_attr = (0x0013, "DATA", stun.pack_bytes, stun.unpack_bytes)
        stun.ATTRIBUTES.append(data_attr)
        stun.ATTRIBUTES_BY_TYPE[0x0013] = data_attr
        stun.ATTRIBUTES_BY_NAME["DATA"] = data_attr

    async def create_permission(self, addr):  # type: ignore[no-untyped-def]
        req = stun.Message(
            message_method=stun.Method.CREATE_PERMISSION,
            message_class=stun.Class.REQUEST,
        )
        req.attributes["XOR-PEER-ADDRESS"] = addr
        await self.request_with_retry(req)

    cls.create_permission = create_permission

    orig_init = cls.__init__

    def patched_init(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        orig_init(self, *args, **kwargs)
        self._permissions = {}

    cls.__init__ = patched_init

    async def patched_send_data(self, data, addr):  # type: ignore[no-untyped-def]
        if addr in self.peer_connect_waiters:
            loop = asyncio.get_event_loop()
            waiter = loop.create_future()
            self.peer_connect_waiters[addr].append(waiter)
            await waiter

        now = time.time()

        if not hasattr(self, "_permissions"):
            self._permissions = {}
        pip = addr[0]
        if pip not in self._permissions or now > self._permissions[pip]:
            try:
                await self.create_permission(addr)
                self._permissions[pip] = now + 240
            except Exception:
                pass

        channel = self.peer_to_channel.get(addr)

        if channel is not None and now <= self.channel_refresh_at.get(channel, 0):
            header = struct.pack("!HH", channel, len(data))
            self._send(header + data)
            return

        if channel is not None:
            try:
                await self.channel_bind(channel, addr)
                self.channel_refresh_at[channel] = now + self.channel_refresh_time
                header = struct.pack("!HH", channel, len(data))
                self._send(header + data)
                return
            except Exception:
                pass

        if channel is None:
            self.peer_connect_waiters[addr] = []
            try:
                new_ch = self.channel_number
                self.channel_number += 1
                await self.channel_bind(new_ch, addr)
                self.channel_refresh_at[new_ch] = now + self.channel_refresh_time
                self.channel_to_peer[new_ch] = addr
                self.peer_to_channel[addr] = new_ch
                for w in self.peer_connect_waiters.pop(addr, []):
                    if not w.done():
                        w.set_result(None)
                header = struct.pack("!HH", new_ch, len(data))
                self._send(header + data)
                return
            except Exception:
                for w in self.peer_connect_waiters.pop(addr, []):
                    if not w.done():
                        w.set_result(None)

        req = stun.Message(message_method=stun.Method.SEND, message_class=stun.Class.INDICATION)
        req.attributes["XOR-PEER-ADDRESS"] = addr
        req.attributes["DATA"] = data
        self._send(bytes(req))

    cls.send_data = patched_send_data

    orig_dgram = cls.datagram_received

    def patched_datagram_received(self, data, addr):  # type: ignore[no-untyped-def]
        data = bytes(data) if not isinstance(data, bytes) else data
        if len(data) >= 4 and turn.is_channel_data(data):
            return orig_dgram(self, data, addr)
        try:
            msg = stun.parse_message(data)
        except ValueError:
            return
        if (
            msg.message_method == stun.Method.DATA
            and msg.message_class == stun.Class.INDICATION
            and self.receiver is not None
        ):
            pa = msg.attributes.get("XOR-PEER-ADDRESS")
            pl = msg.attributes.get("DATA")
            if pa and pl:
                self.receiver.datagram_received(pl, pa)
            return
        return orig_dgram(self, data, addr)

    cls.datagram_received = patched_datagram_received

    cls._patched = True
    logger.info("Patched aioice TURN: CreatePermission + DATA attr + Data indication")
