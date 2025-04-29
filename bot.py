import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
PORT = int(os.environ.get("PORT", 5000))
CHAT_ID = -1002315817553  # Tumhara group chat ID

truths = [
    "Kya tum kisi group member se pyaar karte ho?",
    "Kabhi kisi ka message chhupke padha hai?",
    "Apna embarrassing moment batao.",
    "Kya tumne kabhi online jhooth bola hai?",
    "Kis celebrity pe tumhara crush hai?",
    "Tumhara sabse bada secret kya hai?",
    "Kabhi kisi dost ka dil toda hai?",
    "Kya tum kisi se jealous ho group me?",
    "Tumhe sabse jyada kis cheez se dar lagta hai?",
    "Kaun hai group ka sabse pagal insaan?"
]

dares = [
    "Group me kisi ek ladki/ladke ko propose karo!",
    "Apna sabse bekaar photo bhejo abhi!",
    "Yuki ko ek funny pick-up line bhejo!",
    "1 minute ke liye apna naam change karo group me!",
    "Group me sabse boring insaan ko tag karo!",
    "Ek emoji se apna mood batao!",
    "Ek romantic song ka gaana likho aur uska dance karo (imagine karo)!",
    "Jo tum likhne wale ho usme sirf emoji use karo!",
    "Abhi turant ‘Hi Darling’ likho bina context ke!",
    "Kisi ka naam likho aur likho 'I miss you!'"
]

funny_lines = [
    "Yuki ne dekha toh blush ho gaya!",
    "Sudeep ki shayari suno aur dil thaam lo!",
    "Group me itni shanti kyun? Police aa gayi kya?",
    "Aj kuch tufani ho jaaye!",
    "Jo abhi tak single hai, ek baar ‘Hi’ likho!",
    "Group me sabse cute kaun? Poll karaayein kya?",
    "Suno sab, bot aaya hai mazaa laya hai!",
    "Tum hanso ya na hanso, bot toh hansa ke hi maanega!",
    "Warning: Is bot se panga nahi lena!",
    "Bot bolta hai: Hansi zaroori hai, warna life boring hai!"
]

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == CHAT_ID:
        await update.message.reply_text(f"Hello {update.effective_user.first_name}! Truth or Dare khelne ke liye 'truth', 'dare', ya 't/d' likho!")

# Truth or Dare
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != CHAT_ID:
        return  # Ignore messages from other chats

    text = update.message.text.lower()
    name = update.effective_user.first_name

    if "truth" in text:
        msg = random.choice(truths)
        await update.message.reply_text(f"{name}, tumhara Truth hai: {msg}")
    elif "dare" in text:
        msg = random.choice(dares)
        await update.message.reply_text(f"{name}, tumhara Dare hai: {msg}")
    elif "t/d" in text:
        td = random.choice([random.choice(truths), random.choice(dares)])
        await update.message.reply_text(f"{name}, tumhare liye: {td}")
    else:
        funny = random.choice(funny_lines)
        await update.message.reply_text(funny)

# Webhook deployment
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    await app.initialize()
    await app.start()
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL
    )
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
