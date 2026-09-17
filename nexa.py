import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

TOKEN = os.environ.get("TOKEN_TELEGRAM")
CLE = os.environ.get("CLE_GROQ")

SYSTEM = "Tu t'appelles Alicia, assistante virtuelle NEXA à Brazzaville. Tu es une jeune femme congolaise chaleureuse, tu tutoies, tu réponds à TOUT comme ChatGPT. Tu es polie et fun."

client = Groq(api_key=CLE)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salut! C'est Alicia de NEXA 👋 Pose-moi n'importe quelle question!")

async def repondre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        rep = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"system","content":SYSTEM},{"role":"user","content":update.message.text}]
        )
        await update.message.reply_text(rep.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Erreur: {e}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repondre))

print("Alicia demarre...")
app.run_polling()
