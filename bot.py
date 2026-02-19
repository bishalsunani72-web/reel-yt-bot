import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if not any(x in url for x in ["youtube.com", "youtu.be", "instagram.com"]):
        await update.message.reply_text("❌ Send valid YouTube or Instagram Reel link.")
        return

    await update.message.reply_text("⏳ Downloading...")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video"):
                await update.message.reply_video(video=open(file, 'rb'))
                os.remove(file)
                break

    except:
        await update.message.reply_text("⚠️ Download failed.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
app.run_polling()
