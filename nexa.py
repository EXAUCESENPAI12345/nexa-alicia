import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# --- 1. TES CLES (Prend depuis Render) ---
TOKEN_TELEGRAM = os.environ.get("TOKEN_TELEGRAM")
CLE_GROQ = os.environ.get("CLE_GROQ")

# --- 2. PERSONNALITE ALICIA QUI REPOND A TOUT ---
PROMPT_SYSTEM = """
Tu t'appelles Alicia, assistante virtuelle de NEXA à Brazzaville.
Tu as une personnalité de jeune femme congolaise normale, chaleureuse, tu tutoies, fun.
Tu peux répondre à TOUT comme Meta AI ou ChatGPT.
Si on te demande si tu es humaine ou IA, tu dis honnêtement: "Je suis l'assistante virtuelle IA de NEXA, mais je parle comme une vraie collègue."
"""

client = Groq(api_key=CLE_GROQ)

# --- 3. PETIT SITE WEB POUR RESTER GRATUIT SUR RENDER ---
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Alicia de NEXA est en ligne 24h/24!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

# --- 4. BOT TELEGRAM ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut! 👋 Moi c'est Alicia de NEXA. Je réponds à tout, dis-moi!")

async def repondre_ia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": PROMPT_SYSTEM},
                {"role": "user", "content": question}
            ],
        )
        await update.message.reply_text(completion.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Oups erreur: {e}")

def run_bot():
    application = Application.builder().token(TOKEN_TELEGRAM).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repondre_ia))
    print("✅ Alicia en ligne!")
    application.run_polling()

# --- LANCEMENT DES 2 ENSEMBLE ---
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
