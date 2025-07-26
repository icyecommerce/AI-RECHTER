import os
import logging
import openai
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from memory import save_message, load_conversation

# Logging aan (optioneel voor debugging op Render)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# OpenAI Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Start commando
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Yo, ik ben AI Rechter 2.0. Wat wil je fixen vandaag?")

# Normale berichten
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    user_id = str(update.effective_user.id)

    save_message(user_id, "user", user_message)
    convo = load_conversation(user_id)
    messages = [{"role": "system", "content": open("prompt.txt").read()}] + convo

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    reply = response.choices[0].message.content.strip()
    save_message(user_id, "assistant", reply)
    update.message.reply_text(reply)

# Main bot starter
def main():
    token = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("AI Rechter is live 🔥")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
