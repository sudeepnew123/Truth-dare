import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])

truths = [
    "Tumhara sabse bada sapna kya hai jo abhi tak pura nahi hua?",
    "Kya kabhi tumne apne teacher par crush kiya tha?",
    "Agar koi tumhe propose kare to kya jawab doge?",
    "Kabhi kisi ko apna fake naam bataya hai?",
    "Apni life ka sabse awkward date yaad hai?",
    "Tum apne crush ko secretly stalk karte ho?",
    "Kabhi kisi ko 'I love you' galat samajh ke bol diya?",
    "Agar time travel kar sakte, kis ex ya crush ke paas wapas jaate?",
    "Kya tumhe apne dost ka secret pta hai jo usko nahi pata?",
    "Apne kabhi kisi ko bina bataye follow/unfollow kiya hai?",
    "Tum sabse zyada kisse jealous hote ho group me?",
    "Apna sabse bada pyaar letter ya confession yaad hai?",
    "Kabhi kisi ko bina matlab ke flirt kiya hai?",
    "Agar abhi kiss karne ka mauka mile, kis group member ko select karoge?",
    "Kya tum apne bestfriend se secret pyar karte the ya karti thi?",
    "Agar ek din ke liye opposite gender ban jao to kya karoge?",
    "Kabhi sapne me kisi group wale ko dekha hai?",
    "Apna sabse bada guilty pleasure kya hai?",
    "Tum apne crush ko kis naam se contact save karte ho?",
    "Ek aisi baat jo tum sabse chhupate ho group me?"
]

truths = [
    "Tumhara sabse bada sapna kya hai jo abhi tak pura nahi hua?",
    "Kya kabhi tumne apne teacher par crush kiya tha?",
    "Agar koi tumhe propose kare to kya jawab doge?",
    "Kabhi kisi ko apna fake naam bataya hai?",
    "Apni life ka sabse awkward date yaad hai?",
    "Tum apne crush ko secretly stalk karte ho?",
    "Kabhi kisi ko 'I love you' galat samajh ke bol diya?",
    "Agar time travel kar sakte, kis ex ya crush ke paas wapas jaate?",
    "Kya tumhe apne dost ka secret pta hai jo usko nahi pata?",
    "Apne kabhi kisi ko bina bataye follow/unfollow kiya hai?",
    "Tum sabse zyada kisse jealous hote ho group me?",
    "Apna sabse bada pyaar letter ya confession yaad hai?",
    "Kabhi kisi ko bina matlab ke flirt kiya hai?",
    "Agar abhi kiss karne ka mauka mile, kis group member ko select karoge?",
    "Kya tum apne bestfriend se secret pyar karte the ya karti thi?",
    "Agar ek din ke liye opposite gender ban jao to kya karoge?",
    "Kabhi sapne me kisi group wale ko dekha hai?",
    "Apna sabse bada guilty pleasure kya hai?",
    "Tum apne crush ko kis naam se contact save karte ho?",
    "Ek aisi baat jo tum sabse chhupate ho group me?"
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
