import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ENV
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

# DATA
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
    "Kab last time jhooth bola tha aur kya?",
    "Kya tum group me kisi ko stalk karte ho?",
    "Apna sabse funny nickname batao.",
    "Tumhara pehla crush kaun tha?",
    "Kya tumne kabhi kisi ko secretly like kiya?",
    "Tumne sabse awkward kiss kab aur kahan diya?",
    "Tumhare phone me sabse funny photo kiski hai?",
    "Kya tum kabhi crying emoji me really roye ho?",
    "Kaun hai group ka sabse pagal insaan?",
    "Kya tum apne ex ko yaad karte ho abhi bhi?",
    "Agar tum invisible ho jao to kya karoge?",
    "Apna browser history dikhane me darr lagta hai kya?"
]

dares = [
    "Group me kisi ek ladki/ladke ko propose karo!",
    "Apna sabse bekaar photo bhejo abhi!",
    "Sudeep ke liye ek shayari likho!",
    "Yuki ko ek funny pick-up line bhejo!",
    "Apne phone ka last screenshot bhejo!",
    "1 minute ke liye apna naam change karo group me!",
    "Group me sabse boring insaan ko tag karo!",
    "Ek emoji se apna mood batao!",
    "Koi bhi movie dialogue funny style me likho!",
    "Apna sabse embarrassing song batao jo tum sunte ho!",
    "Apne crush ka naam ulta likho!",
    "3 logon ke funny nickname banao!",
    "Group me sabse zyada active kis par doubt hai? Tag karo!",
    "Ek romantic song ka gaana likho aur uska dance karo (imagine karo)!",
    "Ek sach jo tum kabhi kisi se nahi keh paaye!",
    "Jo tum likhne wale ho usme sirf emoji use karo!",
    "Group me ek insaan chuno jise tum award doge: ‘Drama King/Queen’",
    "Ek ladki ke liye pickup line likho, chahe ladka ho ya ladki!",
    "Apne crush ko message bhejne ki acting karo!",
    "Abhi turant ‘Hi Darling’ likho bina context ke!",
    "Kisi ka naam likho aur likho 'I miss you!'"
]

funny_lines = [
    "Yuki ne dekha toh blush ho gaya!",
    "Sudeep ki shayari suno aur dil thaam lo!",
    "Group me itni shanti kyun? Police aa gayi kya?",
    "Kisiko tag karo warna ghost ban jaoge!",
    "Aj kuch tufani ho jaaye!",
    "Kya aapko bhi lagta hai group me ek spy hai?",
    "Aaj mood romantic hai, dare double milega!",
    "Jisne yeh padha, uski shaadi pe sab invited hai!",
    "Tum hanso ya na hanso, bot toh hansa ke hi maanega!",
    "Sab chup hain, kuch to gadbad hai!",
    "Yuki ka naam sunte hi log online ho jaate hain!",
    "Sudeep = Silent but deadly!",
    "Iss group ka asli hero kaun? Type karo apna naam!",
    "Jo abhi likhega usko dare milega!",
    "Ek like Sudeep ke liye, ek smile Yuki ke liye!",
    "Kya aapko pyaar ho gaya hai? Bot sab jaanta hai!",
    "Group me sabse cute kaun? Poll karaayein kya?",
    "Suno sab, bot aaya hai mazaa laya hai!",
    "Jo abhi tak single hai, ek baar ‘Hi’ likho!",
    "Bot bolta hai: Hansi zaroori hai, warna life boring hai!",
    "Warning: Is bot se panga nahi lena!",
    "Truth & Dare wale ready ho jao, maza aane wala hai!"
]
# FUNCTIONS

async def td(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    action = random.choice(["Truth", "Dare"])
    content = random.choice(truths if action == "Truth" else dares)
    comment = random.choice(funny_lines)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"*{user}*, your turn!\n\n*{action}:* {content}\n\n_{comment}_",
        parse_mode=ParseMode.MARKDOWN
    )

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    content = random.choice(truths)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"*{user}* - Here's your *Truth*:\n{content}",
        parse_mode=ParseMode.MARKDOWN
    )

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    content = random.choice(dares)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"*{user}* - Here's your *Dare*:\n{content}",
        parse_mode=ParseMode.MARKDOWN
    )

async def funny(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(funny_lines))

# Auto Funny Poster
async def send_funny_auto(app):
    bot = app.bot
    line = random.choice(funny_lines)
    await bot.send_message(chat_id=CHAT_ID, text=f"Auto-fun: {line}")

# MAIN
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("td", td))
    app.add_handler(CommandHandler("truth", truth))
    app.add_handler(CommandHandler("dare", dare))
    app.add_handler(CommandHandler("funny", funny))

    # Auto scheduler every 10 mins
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: send_funny_auto(app), "interval", minutes=10)
    scheduler.start()

    # Webhook setup
    webhook_url = f"{RENDER_EXTERNAL_URL}/webhook/{BOT_TOKEN}"
    await app.bot.delete_webhook()
    await app.bot.set_webhook(url=webhook_url)
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_path=f"/webhook/{BOT_TOKEN}",
        url=webhook_url
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
