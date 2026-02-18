import os
import logging
import asyncio
import threading
from flask import Flask
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# 1. LOGGING
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 2. RENDER UCHUN SERVER
server = Flask('')
@server.route('/')
def home(): return "Bot is live!"

def run_server():
    server.run(host='0.0.0.0', port=8080)

# 3. SOZLAMALAR
TELEGRAM_TOKEN = "8359465298:AAE-rcGpOtVlQD9rnYO4UjVenvKP5j9Snd0"
GEMINI_API_KEY = "AIzaSyDC6LzUvitCnKQRa2VXxFmbtKQe4zglbwQ"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. BOT FUNKSIYALARI
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men yangilangan Gemini AI botman. Savol bering!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Model nomini tekshirilgan formatda yuboramiz
        response = model.generate_content(f"Javobni o'zbek tilida ber: {update.message.text}")
        await update.message.reply_text(response.text, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Xato: {e}")
        await update.message.reply_text("Xatolik yuz berdi, qaytadan urinib ko'ring.")

# 5. ASOSIY ISHGA TUSHIRISH (Python 3.14+ uchun moslangan)
async def main():
    # Serverni alohida oqimda boshlash
    threading.Thread(target=run_server, daemon=True).start()
    
    # Bot ilovasini qurish
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # Botni ishga tushirish (Conflict-ni oldini olish uchun drop_updates)
    async with app:
        await app.initialize()
        await app.start()
        print("Bot muvaffaqiyatli ishga tushdi!")
        await app.updater.start_polling(drop_pending_updates=True)
        # Bot to'xtamaguncha kutib turish
        while True:
            await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
