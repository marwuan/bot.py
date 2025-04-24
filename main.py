import telebot
from telebot import types
from flask import Flask
from threading import Thread

# Bot token
TOKEN = '7069051412:AAFfJy-C0yBL0UT4cjxotqSQaoHgpSFc3RM'
# Admin ID for receiving messages
ADMIN_ID = 7632067840

bot = telebot.TeleBot(TOKEN)

# Store user states
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    contact_btn = types.KeyboardButton("📩 تواصل")
    links_btn = types.KeyboardButton("🌐 حساباتي")
    services_btn = types.KeyboardButton("🛠 خدمات")
    markup.add(contact_btn, links_btn, services_btn)
    bot.send_message(message.chat.id, "مرحبا , انا بوت المساعد لمروان , يرجى الاختيار من الاخيارات التالية", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📩 تواصل")
def ask_message(message):
    bot.send_message(message.chat.id, "اكتب الرسالة الي تحب توصلها لمروان:")
    user_states[message.chat.id] = 'waiting_for_message'

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_message')
def forward_message_to_admin(message):
    text = f"رسالة جديدة من @{message.from_user.username or 'بدون معرف'}\n\nالمحتوى:\n{message.text}"
    bot.send_message(ADMIN_ID, text)
    bot.send_message(message.chat.id, "تم إرسال رسالتك إلى مروان، شكراً!")
    user_states.pop(message.chat.id)

# ------------------ قائمة الخدمات ------------------
@bot.message_handler(func=lambda m: m.text == "🛠 خدمات")
def services_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    option1 = types.KeyboardButton("🔧 تصميم بوت")
    option2 = types.KeyboardButton("🌐 تصميم موقع")
    option3 = types.KeyboardButton("Tools 🛠️")
    option4 = types.KeyboardButton("MY Market 🛒")
    back = types.KeyboardButton("⬅️ رجوع")
    markup.add(option1, option2, option3, option4, back)
    bot.send_message(message.chat.id, "اختار نوع الخدمة:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🔧 تصميم بوت")
def bot_design(message):
    bot.send_message(message.chat.id, "تصميم بوت حسب الطلب، تواصل ويانه للتفاصيل.")

@bot.message_handler(func=lambda m: m.text == "🌐 تصميم موقع")
def site_design(message):
    bot.send_message(message.chat.id, "نصمم مواقع احترافية بلغات متعددة.")

@bot.message_handler(func=lambda m: m.text == "Tools 🛠️")
def custom_code(message):
    bot.send_message(message.chat.id, "Soon ...")

@bot.message_handler(func=lambda m: m.text == "MY Market 🛒")
def custom_code(message):
    bot.send_message(message.chat.id, "https://t.me/i30ii")


@bot.message_handler(func=lambda m: m.text == "⬅️ رجوع")
def go_back(message):
    main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📩 تواصل")
    btn2 = types.KeyboardButton("🌐 حساباتي")
    btn3 = types.KeyboardButton("🛠 خدمات")
    main_menu.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "رجعت للقائمة الرئيسية:", reply_markup=main_menu)

# ------------------ روابط التواصل ------------------
@bot.message_handler(func=lambda m: m.text == "🌐 حساباتي")
def send_links(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("تيك توك", url="https://tiktok.com/@j.px"))
    markup.add(types.InlineKeyboardButton("انستغرام", url="https://instagram.com/mrwn"))
    markup.add(types.InlineKeyboardButton("واتساب", url="https://wa.me/9647722727297"))
    markup.add(types.InlineKeyboardButton("يوتيوب", url="https://youtube.com/@your_channel"))
    bot.send_message(message.chat.id, "روابطنا على مواقع التواصل:", reply_markup=markup)

# ------------------ تشغيل السيرفر ------------------
app = Flask('')

@app.route('/')
def home():
    return "البوت شغال"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ------------------ تشغيل البوت ------------------
if __name__ == "__main__":
    keep_alive()
    bot.polling()