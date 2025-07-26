import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from memory import save_message, load_conversation

openai.api_key = os.getenv("OPENAI_API_KEY")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yo, ik ben AI Rechter. Wat wil je fixen vandaag?")

# gewone berichten
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = str(update.effective_user.id)

    # geheugen opslaan
    save_message(user_id, "user", user_message)
    convo = load_conversation(user_id)

    # system prompt + gesprek
    messages = [{"role": "system", "content": open("prompt.txt").read()}] + convo

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    reply = response.choices[0].message.content.strip()
    save_message(user_id, "assistant", reply)
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).bui_
