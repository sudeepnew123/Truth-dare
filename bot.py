import logging
import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

logging.basicConfig(level=logging.INFO)

# Upgraded Truths
truths = [
    "Kya kabhi kisi ko dekh ke raat bhar neend nahi aayi?",
    "Kya group me kisi pe crush hai? Naam lo!",
    "Kya kabhi pyaar me dhokha mila hai?",
    "Kabhi bina brush kiye call pe gaya ho?",
    "Kis ladki/ladke ko secretly stalk karte ho?",
    "Kya kabhi jhooth bola ek date cancel karne ke liye?",
    "Apni sabse embarrassing romantic moment share karo!",
    "Group me kiski smile tumhe sabse pyari lagti hai?",
    "Kabhi kisi ka msg dekh ke blush kiya?",
    "Kya kabhi kisi ko propose karne ka socha hai par himmat nahi hui?"
]

# Upgraded Dares
dares = [
    "Group ki kisi ladki ko propose karo (filmy style me)!",
    "Apne crush ka naam emoji ke sath likho — abhi!",
    "3 baar 'I love you' bolo apne phone ka front cam on karke!",
    "Apna ek funny secret sabke saamne likho!",
    "Kisi ko randomly bolo: 'Mujhe tumse kuch kehna hai...'",
    "Ek romantic shayari group me paste karo!",
    "Group me sabse boring member ko ek comedy nickname do!",
    "Phone gallery se ek embarrassing selfie bhejo!",
    "Ek member ko bolo: 'Main tumhare bina adhura hoon!'",
    "Group me sabko rate karo 1-10 ke beech (based on looks!)"
]

# Store last asked user
last_asked = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey Sudeep! Ready for Truth ya Dare?")

# Handle replies and t/d triggers
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name
    chat_id = str(update.message.chat_id)
    text = update.message.text.lower()

    trigger_words = ["t/d", "truth", "dare", "truth and dare", "play t/d"]

    if any(word in text for word in trigger_words):
        if chat_id in last_asked and last_asked[chat_id] == user_id:
            if "truth" in text:
                await update.message.reply_text(f"{name}, {random.choice(truths)}")
                last_asked.pop(chat_id, None)
                return
            elif "dare" in text:
                await update.message.reply_text(f"{name}, {random.choice(dares)}")
                last_asked.pop(chat_id, None)
                return

        if chat_id not in last_asked:
            last_asked[chat_id] = user_id
            await update.message.reply_text(f"{name}, Truth ya Dare?")
            return

    # If bot is waiting for reply
    if chat_id in last_asked and last_asked[chat_id] == user_id:
        if "truth" in text:
            await update.message.reply_text(f"{name}, {random.choice(truths)}")
            last_asked.pop(chat_id, None)
        elif "dare" in text:
            await update.message.reply_text(f"{name}, {random.choice(dares)}")
            last_asked.pop(chat_id, None)
        else:
            await update.message.reply_text(f"{name}, bas 'truth' ya 'dare' likho!")

# Weekly post
async def weekly_post(app):
    chat_id = int(app.chat_id)
    updates = await app.bot.get_chat_administrators(chat_id)
    users = [admin.user for admin in updates if not admin.user.is_bot]

    if not users:
        return

    selected = random.choice(users)
    name = selected.first_name
    mention = f"@{selected.username}" if selected.username else name

    last_asked[str(chat_id)] = selected.id
    await app.bot.send_message(chat_id, f"{mention}, Truth ya Dare? Reply karo!")

# Main
async def main():
    TOKEN = os.environ["BOT_TOKEN"]
    CHAT_ID = os.environ["CHAT_ID"]

    app = ApplicationBuilder().token(TOKEN).build()
    app.chat_id = CHAT_ID

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: weekly_post(app), "cron", day_of_week="sun", hour=9)
    scheduler.start()


if __name__ == "__main__":
    from telegram.ext import ApplicationBuilder
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # sab handler yahan add karo...

    app.run_polling()  # No await, no async needed
    
  
