import os
import telebot
import openai
from pydub import AudioSegment

# Токены
TELEGRAM_TOKEN = "7643286591:AAEMvq70SCjyhjb6McEWX77rtsXKSnp5O98"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        file = bot.download_file(file_info.file_path)

        # Сохраняем ogg файл
        with open("audio.ogg", "wb") as f:
            f.write(file)

        # Конвертация в mp3
        sound = AudioSegment.from_ogg("audio.ogg")
        sound.export("audio.mp3", format="mp3")

        # Распознавание речи через OpenAI Whisper
        with open("audio.mp3", "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            bot.send_message(message.chat.id, "📝 Расшифровка: " + transcript["text"])
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Ошибка: " + str(e))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Ты написал: " + message.text)

bot.polling()