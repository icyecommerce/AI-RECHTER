import os
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
from memory import save_message, load_conversation

# OpenAI instellen
openai.api_key = os.getenv("OPENAI_API_KEY")

def start(update, context):
    update.message.reply_text("Yo, ik ben AI Rechter. Wat wil je fixen vandaag?")

def handle_message(update, context):
    user_message = update.message.text
    user_id = str(update.effective_user.id)

    save_message(user_id, "user", user_message)
    convo = load_conversation(user_id)
    messages = [{"role": "system", "content": open("prompt.txt").read()}] + convo

    # GPT-4 aanroepen via nieuwe OpenAI lib
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    reply = response.choices[0].message.content.strip()
    save_message(user_id, "assistant", reply)
    update.message.reply_text(reply)

def main():
    updater = Updater(token=os.getenv("TELEGRAM_TOKEN"), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("AI Rechter is live 🔥")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
