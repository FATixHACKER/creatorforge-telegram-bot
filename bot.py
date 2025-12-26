from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from openai import OpenAI
import requests, random, datetime, threading, time

# ================= CONFIG =================
TOKEN = "7110445818:AAHsDEWfNfkzDeY20QrEbbbm1K98oM2H1Qo"
OPENAI_KEY = "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"
DAILY_LIMIT = 5

client = OpenAI(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)

USER_DATA = {}
USER_UI = {}

# ================= HELPERS =================
def get_lang(chat):
    return USER_UI.get(chat, {}).get("lang", "en")

def can_use(chat):
    today = str(datetime.date.today())
    u = USER_DATA[chat]
    if u["date"] != today:
        u["date"] = today
        u["count"] = 0
    if u["count"] >= DAILY_LIMIT:
        return False
    u["count"] += 1
    return True

def ai_text(prompt):
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content

# ================= DARK MENUS =================
def main_menu(chat):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌙 🤖 AI TOOLS", callback_data="ai_menu")],
        [InlineKeyboardButton("📊 DARK ANALYTICS", callback_data="analytics_menu")],
        [InlineKeyboardButton("🛠 PRO TOOLS", callback_data="tools_menu")],
        [InlineKeyboardButton("🌐 LANGUAGE", callback_data="lang_menu")]
    ])

def ai_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ CAPTION", callback_data="ai_caption"),
         InlineKeyboardButton("🎬 SCRIPT", callback_data="ai_script")],
        [InlineKeyboardButton("🎤 VOICE → AI", callback_data="ai_voice"),
         InlineKeyboardButton("🖼 THUMBNAIL", callback_data="thumbnail")],
        [InlineKeyboardButton("⬛ BACK", callback_data="back")]
    ])

def analytics_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 STATS", callback_data="stats"),
         InlineKeyboardButton("📈 ANALYTICS", callback_data="analytics")],
        [InlineKeyboardButton("⚔️ COMPARE", callback_data="compare"),
         InlineKeyboardButton("🏆 LEADERBOARD", callback_data="leaderboard")],
        [InlineKeyboardButton("⬛ BACK", callback_data="back")]
    ])

def tools_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 CALENDAR", callback_data="calendar"),
         InlineKeyboardButton("💬 COMMENTS", callback_data="comment")],
        [InlineKeyboardButton("💰 MONETIZE", callback_data="monetize"),
         InlineKeyboardButton("⏰ REMINDER", callback_data="reminder")],
        [InlineKeyboardButton("⬛ BACK", callback_data="back")]
    ])

def lang_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌙 ENGLISH", callback_data="lang_en"),
         InlineKeyboardButton("🌑 ROMAN URDU", callback_data="lang_ur")],
        [InlineKeyboardButton("⬛ BACK", callback_data="back")]
    ])

# ================= TIKTOK =================
def get_stats(username):
    try:
        r = requests.get(
            f"https://www.tiktok.com/@{username}",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        t = r.text
        followers = int(t.split('"followerCount":')[1].split(',')[0])
        likes = int(t.split('"heart":')[1].split(',')[0])
        return followers, likes
    except:
        return None

# ================= START =================
def start(update, context):
    chat = update.message.chat_id
    USER_DATA.setdefault(chat, {
        "niche": "general",
        "count": 0,
        "date": str(datetime.date.today()),
        "last_username": None
    })
    USER_UI.setdefault(chat, {"lang": "en"})

    update.message.reply_text(
        "🌙 *DARK MODE ACTIVE*\n\n"
        "⬛ PRO AI TELEGRAM BOT\n"
        "⬛ Clean • Fast • Free\n\n"
        "Buttons use karo 👇",
        reply_markup=main_menu(chat),
        parse_mode="Markdown"
    )

# ================= REMINDER =================
def reminder_loop(bot, chat):
    while True:
        time.sleep(86400)
        bot.send_message(chat, "⏰ Reminder jani!\nAaj TikTok video upload karo 🔥")

# ================= BUTTON HANDLER =================
def button_handler(update, context):
    q = update.callback_query
    chat = q.message.chat_id
    data = q.data
    q.answer()

    if data == "back":
        q.message.reply_text("🌙 MAIN MENU", reply_markup=main_menu(chat))

    elif data == "ai_menu":
        q.message.reply_text("🤖 AI TOOLS", reply_markup=ai_menu())

    elif data == "analytics_menu":
        q.message.reply_text("📊 ANALYTICS", reply_markup=analytics_menu())

    elif data == "tools_menu":
        q.message.reply_text("🛠 PRO TOOLS", reply_markup=tools_menu())

    elif data == "lang_menu":
        q.message.reply_text("🌐 LANGUAGE", reply_markup=lang_menu())

    elif data == "lang_en":
        USER_UI[chat]["lang"] = "en"
        q.message.reply_text("🌙 Language set: English", reply_markup=main_menu(chat))

    elif data == "lang_ur":
        USER_UI[chat]["lang"] = "ur"
        q.message.reply_text("🌑 Zaban set: Roman Urdu", reply_markup=main_menu(chat))

    elif data == "ai_caption":
        q.message.reply_text("✍️ Topic bhejo (AI Caption)")

    elif data == "ai_script":
        q.message.reply_text("🎬 Topic bhejo (Video Script)")

    elif data == "ai_voice":
        q.message.reply_text("🎤 Voice note bhejo")

    elif data == "thumbnail":
        hooks = ["99% FAIL 😲", "YEH MAT KARNA!", "SECRET TRICK 🔥"]
        q.message.reply_text(
            f"🖼 THUMBNAIL IDEA\n"
            f"Text: {random.choice(hooks)}\n"
            "Color: Red + Yellow\n"
            "Emotion: Shocked"
        )

    elif data == "calendar":
        today = datetime.date.today()
        plan = "\n".join(
            [f"{today + datetime.timedelta(days=i)} – 1 video @ 8PM" for i in range(7)]
        )
        q.message.reply_text("📅 7-DAY PLAN\n\n" + plan)

    elif data == "comment":
        q.message.reply_text(
            "💬 AUTO COMMENTS\n"
            "🔥 Part 2 chahiye?\n"
            "YES likho agar agree ho\n"
            "Follow for more"
        )

    elif data == "monetize":
        q.message.reply_text(
            "💰 MONETIZATION\n"
            "10k → Brand deals\n"
            "Affiliate\n"
            "Services"
        )

    elif data == "reminder":
        threading.Thread(
            target=reminder_loop,
            args=(context.bot, chat),
            daemon=True
        ).start()
        q.message.reply_text("⏰ Daily reminder ON 🔔")

    elif data == "leaderboard":
        board = sorted(USER_DATA.items(), key=lambda x: x[1]["count"], reverse=True)
        msg = "🏆 LEADERBOARD\n"
        for i, (u, d) in enumerate(board[:5], 1):
            msg += f"{i}. User {u} – {d['count']} uses\n"
        q.message.reply_text(msg)

    elif data == "compare":
        q.message.reply_text("⚔️ Likho:\ncompare user1 user2")

    elif data == "stats":
        q.message.reply_text("📊 TikTok username bhejo")

    elif data == "analytics":
        u = USER_DATA[chat]["last_username"]
        if not u:
            q.message.reply_text("❌ Pehle username bhejo")
            return
        s = get_stats(u)
        if s:
            eng = (s[1] / max(s[0], 1)) * 100
            q.message.reply_text(
                f"📊 ANALYTICS\n"
                f"Followers: {s[0]}\n"
                f"Likes: {s[1]}\n"
                f"Engagement: {eng:.2f}%"
            )

# ================= TEXT / VOICE =================
def handle_text(update, context):
    chat = update.message.chat_id
    text = update.message.text.lower()
    lang = get_lang(chat)

    if text.startswith("caption"):
        if not can_use(chat):
            update.message.reply_text("❌ Daily AI limit reached")
            return
        topic = text.replace("caption", "").strip()
        prompt = (
            f"Roman Urdu mein viral TikTok caption likho about {topic}."
            if lang == "ur"
            else f"Write a viral TikTok caption about {topic} with emojis and CTA."
        )
        update.message.reply_text(ai_text(prompt))

    elif text.startswith("script"):
        topic = text.replace("script", "").strip()
        prompt = f"Write a 30 sec TikTok video script with hook, content, CTA. Topic: {topic}"
        update.message.reply_text(ai_text(prompt))

    else:
        stats = get_stats(text)
        if stats:
            USER_DATA[chat]["last_username"] = text
            update.message.reply_text(
                f"👤 @{text}\nFollowers: {stats[0]}\nLikes: {stats[1]}"
            )

def handle_voice(update, context):
    update.message.reply_text(
        ai_text("Create a viral TikTok caption from a spoken idea.")
    )

# ================= MAIN =================
def main():
    up = Updater(TOKEN, use_context=True)
    dp = up.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.voice, handle_voice))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    up.start_polling()
    up.idle()

main()


