import asyncio
from aioquic.asyncio.client import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.h3.connection import H3_ALPN

arquivos = ["1mb.bin", "10mb.bin", "100mb.bin"]

async def baixar(arquivo):
    configuration = QuicConfiguration(is_client=True, alpn_protocols=H3_ALPN)
    async with connect("localhost", 4433, configuration=configuration) as client:
        stream_id = client._quic.get_next_available_stream_id()
        client._http.send_headers(stream_id, [
            (b":method", b"GET"),
            (b":scheme", b"https"),
            (b":authority", b"localhost"),
            (b":path", f"/{arquivo}".encode()),
        ])
        client.transmit()
        body = b""
        async for event in client._http.events():
            if hasattr(event, 'data'):
                body += event.data
        print(f"{arquivo}: baixado {len(body)} bytes")

async def main():
    for arq in arquivos:
        await baixar(arq)

asyncio.run(main())
