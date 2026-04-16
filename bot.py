import telebot
from config import BOT_TOKEN, CHAT_ID
from reader import read_pdf, read_website, read_text
from ai import generate_qa
from database import add_questions, get_question
from scheduler import start_scheduler, can_send

bot = telebot.TeleBot(BOT_TOKEN)

# 📥 LOAD CONTENT (edit here)
def load_content():
    # OPTION 1: PDF
    # text = read_pdf("notes.pdf")

    # OPTION 2: WEBSITE
    text = read_website("https://example.com")

    # OPTION 3: TEXT
    # text = read_text("Your notes here")

    qa = generate_qa(text)
    add_questions(qa)

# 📤 SEND FUNCTION
def send_revision():
    if not can_send():
        return

    q = get_question()
    bot.send_message(CHAT_ID, q)

# 🚀 START
load_content()
start_scheduler(send_revision)

print("🤖 Bot Running...")
bot.infinity_polling()
