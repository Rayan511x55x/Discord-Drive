import discord
from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import threading
import base64
from io import BytesIO
from datetime import datetime

TOKEN = "YOUR-BOT-TOKEN"
CHANNEL_ID = 123456789  # your Discord channel ID, for the database or the storage container 

intents = discord.Intents.default()
intents.messages = True
bot = discord.Client(intents=intents)
app = Flask(__name__)
CORS(app)

message_queue = asyncio.Queue()

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json
    message = data.get("message", "")
    filename = data.get("filename")
    filedata = data.get("filedata")  # base64 string with header

    if not (filename and filedata):
        return jsonify({"error": "Missing filename or filedata"}), 400

    file_bytes = base64.b64decode(filedata.split(",")[1])
    payload = {
        "text": message,
        "file": (filename, file_bytes)
    }
    asyncio.run_coroutine_threadsafe(message_queue.put(payload), bot.loop)
    return jsonify({"status": "queued"}), 200

@app.route("/files", methods=["GET"])
def list_files():
    async def fetch():
        channel = bot.get_channel(CHANNEL_ID)
        messages = [msg async for msg in channel.history(limit=100)]
        results = []
        for msg in reversed(messages):
            for a in msg.attachments:
                results.append({
                    "id": msg.id,
                    "filename": a.filename,
                    "content_type": a.content_type,
                    "download_url": a.url,
                    "uploaded_at": msg.created_at.isoformat()
                })
        return results

    future = asyncio.run_coroutine_threadsafe(fetch(), bot.loop)
    return jsonify(future.result())

@app.route("/delete", methods=["DELETE"])
def delete():
    data = request.json
    msg_id = data.get("id")

    if not msg_id:
        return jsonify({"error": "No message ID"}), 400

    async def do_delete():
        try:
            channel = bot.get_channel(CHANNEL_ID)
            msg = await channel.fetch_message(int(msg_id))
            await msg.delete()
            return True
        except Exception as e:
            print("Delete failed:", e)
            return False

    future = asyncio.run_coroutine_threadsafe(do_delete(), bot.loop)
    success = future.result()
    return jsonify({"status": "deleted" if success else "failed"})

@app.route("/rename", methods=["PUT"])
def rename():
    data = request.json
    msg_id = data.get("id")
    new_name = data.get("new_name")

    async def do_rename():
        try:
            channel = bot.get_channel(CHANNEL_ID)
            msg = await channel.fetch_message(int(msg_id))
            if not msg.attachments:
                return False
            a = msg.attachments[0]
            content = msg.content + f" [Renamed to: {new_name}]"
            await msg.delete()
            file = await a.read(use_cached=True)
            await channel.send(content, file=discord.File(BytesIO(file), filename=new_name))
            return True
        except Exception as e:
            print("Rename failed:", e)
            return False

    future = asyncio.run_coroutine_threadsafe(do_rename(), bot.loop)
    success = future.result()
    return jsonify({"status": "renamed" if success else "failed"})

@app.route("/files", methods=["GET"])
def get_list_files():
    async def fetch():
        channel = bot.get_channel(CHANNEL_ID)
        messages = [msg async for msg in channel.history(limit=100)]
        results = []
        for msg in reversed(messages):
            for a in msg.attachments:
                results.append({
                    "id": str(msg.id),
                    "filename": a.filename,
                    "content_type": a.content_type,
                    "download_url": a.url,
                    "uploaded_at": msg.created_at.isoformat()
                })
        return results

    future = asyncio.run_coroutine_threadsafe(fetch(), bot.loop)
    return jsonify(future.result())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    while True:
        payload = await message_queue.get()
        text = payload["text"]
        filename, file_bytes = payload["file"]
        file_obj = BytesIO(file_bytes)
        file = discord.File(fp=file_obj, filename=filename)
        await channel.send(content=text or "Uploaded file:", file=file)

def run_flask():
    app.run(host="0.0.0.0", port=5000)

threading.Thread(target=run_flask).start()
bot.run(TOKEN)
