import telebot
import yt_dlp
import os
from flask import Flask
import threading

# Token bot lu
TOKEN = '8838743968:AAGjIYur0Haoy5j-Btb8XR1oVfdTdM5f6Z4'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Ini web server bohong-bohongan biar cloud-nya seneng
@app.route('/')
def home():
    return "Bot is running 24/7 bro!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo bro! 🤙 Kirim link sosmed apa aja (IG, YT, TikTok, X, dll) ke gw, nanti gw downloadin.")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text
    if not url.startswith("http"):
        bot.reply_to(message, "Bro, kirim link yang bener yak (pake http/https)!")
        return

    msg = bot.reply_to(message, "Sabar yak, lagi gw proses (otw download)... ⏳")
    ydl_opts = {'outtmpl': 'downloaded_video.%(ext)s', 'format': 'best', 'quiet': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)

        bot.delete_message(message.chat.id, msg.message_id)
        os.remove(filename)
    except Exception as e:
        bot.reply_to(message, f"Yah gagal bro. Error: {str(e)}")

# Fungsi buat nyalain bot di latar belakang
def run_bot():
    bot.polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    # Port dari cloud server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
