import os
import json
import socket
import random
import asyncio
import aiohttp

# 전역 변수 (초기값)
host = os.getenv("HOST", "http://localhost")
port = os.getenv("PORT", "8000")
name = socket.gethostname()

def generate_payload():
    temp = random.randint(0, 100)
    status = "safe" if temp <= 70 else "danger"
    return {
        "name": name,
        "temperature": temp,
        "status": status
    }

async def update_config():
    global host, port, name
    while True:
        host = os.getenv("HOST", "http://localhost")
        port = os.getenv("PORT", "8000")
        name = socket.gethostname()
        print(f"[Config Updated] host={host}, port={port}, name={name}")
        await asyncio.sleep(60)  # 60초마다 갱신

async def send_data():
    global host, port
    while True:
        url = f"{host}:{port}/"
        payload = generate_payload()
        print(f"[Sending data] {url}: {payload}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    print(f"[Response] {resp.status}")
        except Exception as e:
            print(f"Error sending data: {e}")

        await asyncio.sleep(10)  # 10초마다 전송

async def main():
    await asyncio.gather(
        update_config(),
        send_data()
    )

if __name__ == "__main__":
    asyncio.run(main())
