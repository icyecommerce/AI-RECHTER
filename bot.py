import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
from memory import save_message, load_conversation
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start(update, context):
    update.message.reply_text("Yo, ik ben AI Rechter. Laat me weten wat je wil fixen.")

def handle_message(update, context):
    user_message = update.message.text
    user_id = str(update.effective_user.id)

    # 1. Save user message
    save_message(user_id, "user", user_message)

    # 2. Load full convo
    convo = [
    msg for msg in load_conversation(user_id)
    if "[GEHEUGEN]" not in msg["content"]
]
    messages = [{"role": "system", "content": open("prompt.txt").read()}] + convo

    # 3. Laat AI Rechter reageren
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    reply = response.choices[0].message.content.strip()

    # 4. Stuur reactie terug & sla op
    update.message.reply_text(reply)
    save_message(user_id, "assistant", reply)

    # 5. EXTRA: auto-learning check
    memory_check = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Analyseer dit bericht. Bevat het nuttige info over wie de gebruiker is, wat hij doet, zijn doelen of samenwerkingen? Als ja, vat het dan samen in 1 korte zin. Als nee, zeg dan letterlijk: 'niets'."},
            {"role": "user", "content": user_message}
        ]
    )

    memory_output = memory_check.choices[0].message.content.strip()

    if "niets" not in memory_output.lower():
        # Supabase accepteert alleen geldige rollen zoals 'system'
        save_message(user_id, "system", f"(GEHEUGEN): {memory_output}")
        print(f"🧠 Opgeslagen in geheugen: {memory_output}")
    else:
        print("⛔ Geen relevante info om op te slaan.")

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
