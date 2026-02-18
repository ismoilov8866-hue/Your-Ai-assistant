import os
import logging
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# Logging sozlamalari (xatolarni ko'rish uchun)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Kalitlarni olish
TELEGRAM_TOKEN = "8359465298:AAE-rcGpOtVlQD9rnYO4UjVenvKP5j9Snd0"
GROQ_API_KEY = "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"

# Grok mijozini sozlash
client = Groq(api_key=GROQ_API_KEY)

# AI uchun tizim ko'rsatmasi (System Prompt)
SYSTEM_PROMPT = """Siz universal mutaxassis yordamchisiz. 
1. Foydalanuvchining har qanday sohadagi savoliga javob bering.
2. Agar ma'lumot taqqoslash yoki ro'yxat bo'lsa, uni ALBATTA Markdown jadval ko'rinishida taqdim eting.
3. Javoblaringizni o'zbek tilida bering.
4. Jadvallar Telegramda chiroyli ko'rinishi uchun Markdown formatidan to'g'ri foydalaning."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men Grok AI asosidagi botman. Menga xohlagan savolingizni bering, men uni tahlil qilib (hatto jadvallar bilan) javob beraman.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # Grok AI dan javob olish
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            model="llama3-70b-8192", # Groq-dagi eng kuchli model
            temperature=0.7,
        )
        
        ai_reply = chat_completion.choices[0].message.content
        
        # Javobni yuborish
        await update.message.reply_text(ai_reply, parse_mode='Markdown')
        
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        await update.message.reply_text("Kechirasiz, javob tayyorlashda xatolik yuz berdi. Birozdan so'ng urinib ko'ring.")

if __name__ == '__main__':
    # Botni ishga tushirish
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot muvaffaqiyatli ishga tushdi...")
    app.run_polling()
from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()
