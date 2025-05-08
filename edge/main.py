import os
import json
import socket
import random
import asyncio
import aiohttp
import time
import threading
from flask import Flask, request, jsonify

print("Container Init...")
time.sleep(5)

# 전역 변수
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
        host = os.getenv("HOST", host)
        port = os.getenv("PORT", port)
        name = socket.gethostname()
        print(f"[Config Updated] host={host}, port={port}, name={name}", flush=True)
        await asyncio.sleep(60)

async def send_data():
    global host, port
    while True:
        url = f"{host}:{port}/"
        payload = generate_payload()
        print(f"[Sending data] {url}: {payload}", flush=True)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    print(f"[Response] {resp.status}", flush=True)
        except Exception as e:
            print(f"[Sending Error] {e}", flush=True)

        await asyncio.sleep(10)

def run_flask_app():
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    @app.route("/config", methods=["POST"])
    def set_config():
        global host, port
        data = request.get_json()
        updated = {}

        if "host" in data:
            host = data["host"]
            updated["host"] = host
        if "port" in data:
            port = data["port"]
            updated["port"] = port
            print(f"[Flask] CONFIG updated to: {updated}", flush=True)

        return jsonify({"status": "updated", **updated})
    
    print("[Flask] Running Flask App")
    app.run(host="0.0.0.0", port=5000)

async def main():
    threading.Thread(target=run_flask_app, daemon=True).start()
    await asyncio.gather(
        # update_config(),
        send_data()
    )

if __name__ == "__main__":
    print("Running main thread", flush=True)
    asyncio.run(main())
