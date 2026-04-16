import telebot
import time

from config import BOT_TOKEN
from database import (
    add_user,
    add_questions,
    get_revision,
    update_question,
    save_memory,
    get_memory
)
from reader import read_pdf, read_website
from ai import generate_qa, ask_ai
from scheduler import start

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# ✅ START COMMAND (only once needed)
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    add_user(user_id)
    bot.reply_to(message, "✅ AI Revision Bot Activated")


# ✅ TEXT / LINK / CHATBOT
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        user_id = message.from_user.id
        text = message.text.strip()

        # save user input
        save_memory(user_id, f"user: {text}")

        # 🌐 WEBSITE MODE
        if "http" in text:
            content = read_website(text)

            if not content:
                bot.reply_to(message, "❌ Failed to read website")
                return

            qa = generate_qa(content)

            if qa:
                add_questions(user_id, qa)
                bot.reply_to(message, "✅ Content added for revision")
            else:
                bot.reply_to(message, "❌ AI failed to generate Q&A")
            return

        # 🤖 CHATBOT MODE
        memory = get_memory(user_id)
        answer = ask_ai(memory, text)

        save_memory(user_id, f"bot: {answer}")

        bot.reply_to(message, answer)

    except Exception as e:
        print("TEXT ERROR:", e)
        bot.reply_to(message, "⚠️ Error occurred")


# ✅ PDF HANDLER
@bot.message_handler(content_types=['document'])
def handle_pdf(message):
    try:
        file = bot.get_file(message.document.file_id)
        data = bot.download_file(file.file_path)

        path = "temp.pdf"
        with open(path, "wb") as f:
            f.write(data)

        text = read_pdf(path)

        if not text:
            bot.reply_to(message, "❌ Could not read PDF")
            return

        qa = generate_qa(text)

        if qa:
            add_questions(message.from_user.id, qa)
            bot.reply_to(message, "✅ PDF processed & added")
        else:
            bot.reply_to(message, "❌ AI failed")

    except Exception as e:
        print("PDF ERROR:", e)
        bot.reply_to(message, "⚠️ Error processing PDF")


# ✅ REVISION SENDER
def send_revision_to_user(user_id):
    try:
        qs = get_revision(user_id)

        if not qs:
            return

        for q in qs:
            bot.send_message(
                user_id,
                f"📚 <b>Revision</b>\n\n{q['text']}"
            )
            update_question(q)

    except Exception as e:
        print("SEND ERROR:", e)


# ✅ START SCHEDULER (FIXED)
start(send_revision_to_user)

print("🤖 Running V3 AI Bot...")


# ✅ CRASH SAFE POLLING (IMPORTANT 🔥)
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=30)
    except Exception as e:
        print("POLLING ERROR:", e)
        time.sleep(10)
