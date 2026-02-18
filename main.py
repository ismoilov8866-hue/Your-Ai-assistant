import os
import logging
import threading
from flask import Flask
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# 1. LOGGING
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 2. RENDER UCHUN VEB-SERVER (Bot o'chib qolmasligi uchun)
server = Flask('')

@server.route('/')
def home():
    return "Gemini Bot ishlayapti!"

def run_server():
    server.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run_server)
    t.start()

# 3. KALITLAR
TELEGRAM_TOKEN = "8359465298:AAE-rcGpOtVlQD9rnYO4UjVenvKP5j9Snd0"
GEMINI_API_KEY = "AIzaSyDC6LzUvitCnKQRa2VXxFmbtKQe4zglbwQ"

# Gemini AI-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
# Eng yangi va kuchli model: gemini-1.5-pro yoki gemini-1.5-flash
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. AI SOZLAMALARI
SYSTEM_PROMPT = """Siz universal mutaxassis yordamchisiz. 
1. Har qanday sohadagi savolga javob bering.
2. Agar ma'lumot ro'yxat yoki taqqoslash bo'lsa, uni ALBATTA Markdown jadval ko'rinishida taqdim eting.
3. Javoblaringizni o'zbek tilida bering.
4. Jadvallar Telegramda chiroyli ko'rinishi uchun Markdown formatidan foydalaning."""

# 5. BOT FUNKSIYALARI
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men Google Gemini AI asosidagi botman. Menga savol bering, men jadvallar bilan javob beraman!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # Gemini-ga so'rov yuborish
        full_prompt = f"{SYSTEM_PROMPT}\n\nFoydalanuvchi savoli: {user_text}"
        response = model.generate_content(full_prompt)
        
        ai_reply = response.text
        
        # Javobni yuborish
        await update.message.reply_text(ai_reply, parse_mode='Markdown')
        
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await update.message.reply_text("Kechirasiz, Gemini modelini ulashda xatolik yuz berdi.")

# 6. ASOSIY ISHGA TUSHIRISH
if __name__ == '__main__':
    keep_alive()
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Gemini Bot muvaffaqiyatli ishga tushdi...")
    app.run_polling()
