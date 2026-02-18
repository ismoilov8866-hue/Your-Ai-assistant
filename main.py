import os
import logging
import threading
from flask import Flask
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from dotenv import load_dotenv

# .env yuklash
load_dotenv()

# Logging sozlamalari
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Render uchun server
server = Flask('')
@server.route('/')
def home(): 
    return "Bot is running!"

def run_server(): 
    server.run(host='0.0.0.0', port=8080)

# Kalitlarni xavfsiz olish
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8359465298:AAE-rcGpOtVlQD9rnYO4UjVenvKP5j9Snd0")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDC6LzUvitCnKQRa2VXxFmbtKQe4zglbwQ")

# Gemini AI-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)

# DIQQAT: Model nomi 'models/gemini-1.5-flash' ko'rinishida bo'lishi kerak
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men Gemini AI botman. Savol bering!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Tizimli ko'rsatma bilan birga yuborish
        response = model.generate_content(f"Javobni o'zbek tilida va jadvallar bilan ber: {update.message.text}")
        await update.message.reply_text(response.text, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Xato yuz berdi: {e}")
        await update.message.reply_text("Kechirasiz, javob olishda xatolik yuz berdi.")

if __name__ == '__main__':
    # Serverni alohida oqimda ishga tushirish
    threading.Thread(target=run_server).start()
    
    # Botni yaratish
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot ishga tushdi...")
    
    # drop_pending_updates=True -> Conflict xatosini oldini olish uchun
    app.run_polling(drop_pending_updates=True)
