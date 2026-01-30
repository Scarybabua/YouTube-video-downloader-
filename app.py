import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from yt_dlp import YoutubeDL
import os

# --- API डिटेल्स (इनको प्लेटफॉर्म की Settings में 'Secrets' में भरें) ---
API_ID = int(os.environ.get("API_ID", 20301186))
API_HASH = os.environ.get("API_HASH", "924bf76387428a6140550b45b1b8979f")
SESSION_STRING = os.environ.get("SESSION_STRING", "BQE1xYIAMACoAGTDtIn-vPaBA9m7Zv-NFrMKwJljJxMzM8rGwCR_48JE1o1ZzhqlJFUiHKVOBnCaycCdWQE0gW7MZFc2oeUtKOA7SGOHS5NrbJX1uH_Ev7mycBGq2yd7U4mBWI42bo7lHwrbTqH2id9kXBfij2-fSOyKttCUsmxxD8ybhLKNSp1qcAH_OzIDvzzh4ywptyMNs-nvr4eCc-cDmEVy96-QSbbCKBXB79GZfVHGHzgpyuuIq2T8LfrKj4VwsqPR3j5CwTgfrNYBkF-DYcMrNfwy_bOrwB_XY-yPXvwrMi8W9WSOHxX8SBMG-wVYoHmSY0Qj4BcQfeptLLwY306kHAAAAAFqiMZ6AA")

# क्लाइंट सेटअप
app = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call_py = PyTgCalls(app)

# YouTube सर्च सेटिंग्स
YDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "default_search": "ytsearch",
    "nocheckcertificate": True
}

# 1. /play कमांड
@app.on_message(filters.command("play") & filters.group)
async def play_audio(_, message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("❌ गाने का नाम लिखें (जैसे: /play hum katha sunate)")
    
    m = await message.reply("🔎 खोज रहा हूँ...")
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(query, download=False)['entries'][0]
            url = info['url']
        
        await call_py.play(message.chat.id, MediaStream(url, video_flags=False))
        await m.edit(f"🎶 **बज रहा है:** {info['title']}")
    except Exception as e:
        await m.edit(f"❌ एरर: {e}")

# 2. /stop कमांड
@app.on_message(filters.command("stop") & filters.group)
async def stop_stream(_, message):
    try:
        await call_py.leave_call(message.chat.id)
        await message.reply("⏹ गाना बंद कर दिया गया है।")
    except:
        await message.reply("❌ कोई कॉल चालू नहीं है।")

# बोट शुरू करने का फंक्शन
async def run_bot():
    await app.start()
    await call_py.start()
    print("✅ बोट अब ग्रुप में गाने बजाने के लिए तैयार है!")
    await asyncio.idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
