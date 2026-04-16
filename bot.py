import telebot
import time

from config import BOT_TOKEN, CHAT_ID
from reader import read_website
from ai import generate_qa
from database import add_questions, get_question
from scheduler import start_scheduler, can_send

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# 🔥 LOAD CONTENT (EDIT THIS)
def load_content():
    print("Loading content...")

    text = read_website("https://example.com")

    if not text:
        print("No content found")
        return

    qa = generate_qa(text)

    if qa:
        add_questions(qa)
        print("Q&A Generated")
    else:
        print("AI failed")


# 📤 SEND FUNCTION
def send_revision():
    try:
        if not can_send():
            return

        q = get_question()

        if not q:
            bot.send_message(CHAT_ID, "⚠️ No questions available yet")
            return

        bot.send_message(CHAT_ID, f"📚 Revision Time:\n\n{q}")

    except Exception as e:
        print("SEND ERROR:", e)


# 🚀 START SYSTEM
if __name__ == "__main__":
    load_content()
    start_scheduler(send_revision)

    print("🤖 Bot Running...")

    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as e:
            print("Polling Error:", e)
            time.sleep(10)
