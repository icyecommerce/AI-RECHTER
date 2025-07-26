import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from memory import save_message, load_conversation
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yo, ik ben AI Rechter. Wat wil je fixen vandaag?")

# gewone berichten
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = str(update.effective_user.id)

    save_message(user_id, "user", user_message)
    convo = load_conversation(user_id)
    messages = [{"role": "system", "content": open("prompt.txt").read()}] + convo

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    reply = response.choices[0].message.content.strip()
    save_message(user_id, "assistant", reply)
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("AI Rechter is live 🔥")
    app.run_polling()

if __name__ == "__main__":
    main()
