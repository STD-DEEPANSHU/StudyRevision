import telebot
import os

from config import BOT_TOKEN
from database import save_user, add_question, get_question
from reader import read_pdf, read_website
from ocr import read_image
from ai import generate_qa
from scheduler import start

bot = telebot.TeleBot(BOT_TOKEN)

# 📩 START
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    save_user(user_id)
    bot.reply_to(message, "✅ You are registered for auto revision!")

# 📄 HANDLE TEXT / LINK
@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    text = message.text

    if "http" in text:
        content = read_website(text)
    else:
        content = text

    qa = generate_qa(content)

    if qa:
        add_question(user_id, qa)
        bot.reply_to(message, "✅ Questions generated!")
    else:
        bot.reply_to(message, "❌ AI failed")

# 📄 HANDLE PDF
@bot.message_handler(content_types=['document'])
def handle_doc(message):
    file = bot.get_file(message.document.file_id)
    downloaded = bot.download_file(file.file_path)

    path = f"{message.document.file_name}"
    with open(path, "wb") as f:
        f.write(downloaded)

    text = read_pdf(path)
    qa = generate_qa(text)

    if qa:
        add_question(message.from_user.id, qa)
        bot.reply_to(message, "✅ PDF processed!")

# 🖼 IMAGE OCR
@bot.message_handler(content_types=['photo'])
def handle_img(message):
    file = bot.get_file(message.photo[-1].file_id)
    downloaded = bot.download_file(file.file_path)

    path = "img.jpg"
    with open(path, "wb") as f:
        f.write(downloaded)

    text = read_image(path)
    qa = generate_qa(text)

    if qa:
        add_question(message.from_user.id, qa)
        bot.reply_to(message, "✅ Image processed!")

# 📤 SEND REVISION
def send_revision_to_user(user_id):
    q = get_question(user_id)
    if q:
        bot.send_message(user_id, f"📚 Revision:\n\n{q}")

# 🚀 START
start()
print("🤖 Running...")
bot.infinity_polling()
