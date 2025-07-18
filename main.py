import os
import telebot
import openai
from pydub import AudioSegment

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        file = bot.download_file(file_info.file_path)

        with open("audio.ogg", "wb") as f:
            f.write(file)

        sound = AudioSegment.from_ogg("audio.ogg")
        sound.export("audio.mp3", format="mp3")

        with open("audio.mp3", "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            bot.send_message(message.chat.id, "📝 Расшифровка: " + transcript["text"])
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Ошибка: " + str(e))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Ты написал: " + message.text)

bot.polling()