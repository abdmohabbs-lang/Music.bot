import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("BOT_TOKEN missing!")
    exit()

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text.startswith("يوت"):
        query = text.replace("يوت", "").strip()

        if not query:
            await update.message.reply_text("اكتب اسم المقطع")
            return

        await update.message.reply_text("جاري التحميل 🎧")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'song.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(f"ytsearch1:{query}", download=True)

            for f in os.listdir():
                if f.endswith(".mp3"):
                    with open(f, "rb") as audio:
                        await update.message.reply_audio(audio)
                    os.remove(f)

        except Exception as e:
            print("ERROR:", e)
            await update.message.reply_text("صار خطأ ❌")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot is running...")
app.run_polling()
