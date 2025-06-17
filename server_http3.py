import asyncio
import ssl
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import ProtocolNegotiated
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.h3.events import HeadersReceived, DataReceived
import os

class HTTP3ServerProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._http = H3Connection(self._quic)

    def quic_event_received(self, event):
        self._http.handle_event(event)

        for http_event in self._http.events():
            if isinstance(http_event, HeadersReceived):
                path = http_event.headers[1][1].decode()
                filename = path.strip("/")
                try:
                    with open(os.path.join("files", filename), "rb") as f:
                        data = f.read()
                    self._http.send_headers(http_event.stream_id, [(b":status", b"200")])
                    self._http.send_data(http_event.stream_id, data, end_stream=True)
                except FileNotFoundError:
                    self._http.send_headers(http_event.stream_id, [(b":status", b"404")])
                    self._http.send_data(http_event.stream_id, b"Not found", end_stream=True)

async def main():
    configuration = QuicConfiguration(
        alpn_protocols=H3_ALPN,
        is_client=False,
        max_datagram_frame_size=65536,
    )
    configuration.load_cert_chain("cert.pem", "key.pem")

    await serve("0.0.0.0", 4433, configuration=configuration, create_protocol=HTTP3ServerProtocol)

if __name__ == "__main__":
    asyncio.run(main())
