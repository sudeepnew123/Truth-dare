import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])

truths = [
    "Kya tumne kabhi kisi ko chhupkar stalk kiya hai?",
    "Kya tum abhi kisi pe crush rakhte ho?",
    "Kabhi kisi ko bina bataye kiss kiya hai?",
    "Kya tumne kabhi girlfriend/boyfriend se jhooth bola hai?",
    "Kis group member ko tum secretly pasand karte ho?"
]

dares = [
    "Group mein jispe crush hai usko propose karo (acting sahi honi chahiye!)",
    "Ek ladka ya ladki ko pyaar bhara message bhejo",
    "Apna funny selfie bhejo abhi!",
    "Ek shayari ya song gao yahan sabke liye",
    "Bina context ke 'I love you' kisi ko bhejo"
]

async def td(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.id != CHAT_ID:
        return

    members = await context.bot.get_chat_administrators(update.message.chat_id)
    all_members = [admin.user for admin in members if not admin.user.is_bot]
    if not all_members:
        await update.message.reply_text("Kisi ka naam nahi mila! Group mein log hi nahi?")
        return

    target = random.choice(all_members)
    t_or_d = random.choice(["Truth", "Dare"])
    prompt = random.choice(truths if t_or_d == "Truth" else dares)

    await update.message.reply_text(
        f"{target.mention_html()} — *{t_or_d}*\n{prompt}",
        parse_mode="HTML"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("td", td))
    app.run_polling()
