import os
import logging
import threading
from flask import Flask
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# 1. LOGGING (Xatolarni kuzatish uchun)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 2. RENDER UCHUN VEB-SERVER (Bot o'chib qolmasligi uchun)
server = Flask('')

@server.route('/')
def home():
    return "Bot ishlayapti!"

def run_server():
    server.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run_server)
    t.start()

# 3. KALITLAR (Render Environment Variables'dan oladi)
# Agar Renderda xatolik bersa, bu yerga to'g'ridan-to'g'ri qo'ysangiz ham bo'ladi
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8359465298:AAE-rcGpOtVlQD9rnYO4UjVenvKP5j9Snd0")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

# Groq mijozini sozlash
client = Groq(api_key=GROQ_API_KEY)

# 4. AI SOZLAMALARI (System Prompt)
SYSTEM_PROMPT = """Siz universal mutaxassis yordamchisiz. 
1. Har qanday sohadagi savolga javob bering.
2. Agar ma'lumot ro'yxat yoki taqqoslash bo'lsa, uni ALBATTA Markdown jadval ko'rinishida taqdim eting.
3. Javoblaringizni o'zbek tilida bering.
4. Jadvallar Telegramda buzilmasligi uchun Markdown formatidan to'g'ri foydalaning."""

# 5. BOT FUNKSIYALARI
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men eng kuchli Llama 3.3 AI modeliga ulangan botman. Menga savol bering, men jadvallar bilan javob beraman!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # ENG KUCHLI MODEL: llama-3.3-70b-versatile
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.6,
        )
        
        ai_reply = chat_completion.choices[0].message.content
        
        # Javobni yuborish (MarkdownV2 jadvallar uchun eng yaxshisi)
        await update.message.reply_text(ai_reply, parse_mode='Markdown')
        
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await update.message.reply_text("Kechirasiz, modelni ulashda xatolik yuz berdi. API kalitini tekshiring.")

# 6. ASOSIY ISHGA TUSHIRISH
if __name__ == '__main__':
    # Veb-serverni alohida oqimda ishga tushirish
    keep_alive()
    
    # Telegram botni ishga tushirish
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot muvaffaqiyatli ishga tushdi...")
    app.run_polling()
