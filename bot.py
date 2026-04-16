import telebot

from config import BOT_TOKEN
from database import add_user, add_questions, get_revision, update_question, save_memory, get_memory
from reader import read_pdf, read_website
from ai import generate_qa, ask_ai
from scheduler import start

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start_cmd(message):
    add_user(message.from_user.id)
    bot.reply_to(message, "✅ AI Revision Bot Activated")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    text = message.text

    save_memory(user_id, f"user: {text}")

    # WEBSITE
    if "http" in text:
        content = read_website(text)
        qa = generate_qa(content)

        if qa:
            add_questions(user_id, qa)
            bot.reply_to(message, "✅ Content added for revision")
        return

    # CHATBOT
    memory = get_memory(user_id)
    answer = ask_ai(memory, text)

    save_memory(user_id, f"bot: {answer}")
    bot.reply_to(message, answer)


@bot.message_handler(content_types=['document'])
def handle_pdf(message):
    file = bot.get_file(message.document.file_id)
    data = bot.download_file(file.file_path)

    with open("temp.pdf", "wb") as f:
        f.write(data)

    text = read_pdf("temp.pdf")
    qa = generate_qa(text)

    if qa:
        add_questions(message.from_user.id, qa)
        bot.reply_to(message, "✅ PDF processed & added")


def send_revision_to_user(user_id):
    qs = get_revision(user_id)

    for q in qs:
        bot.send_message(user_id, f"📚 <b>Revision</b>\n\n{q['text']}")
        update_question(q)


start()
print("🤖 Running V3 AI Bot...")
bot.infinity_polling()
