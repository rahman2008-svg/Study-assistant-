import os
import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# Render-এর ফ্রি টায়ারের জন্য ছোট একটি ওয়েব সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "বটটি অনলাইনে আছে!"

def run():
    # Render সাধারণত ১০০০০ পোর্ট ব্যবহার করে
    app.run(host='0.0.0.0', port=10000)

# আপনার দেওয়া টোকেন এবং এপিআই কী
BOT_TOKEN = "8223615159:AAHmqJY28w4t7J-kEf5GB_LNthUWJ0IpXBU"
GROQ_API_KEY = "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"

# বট এবং Groq ক্লায়েন্ট সেটআপ
bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# কেউ /start দিলে আপনার নামসহ স্বাগতম জানাবে
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "হ্যালো! আমি আপনার স্টাডি অ্যাসিস্ট্যান্ট।\n\n"
        "🤖 আমি আব্দুর রহমান, আমি এই বটটি তৈরি করেছি।"
    )
    bot.reply_to(message, welcome_text)

# চ্যাট রিপ্লাই দেওয়ার মূল ফাংশন
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Groq API ব্যবহার করে উত্তর তৈরি
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": message.text}
            ],
            model="llama3-8b-8192",
        )
        
        # এআই-এর উত্তর
        ai_response = chat_completion.choices[0].message.content
        
        # উত্তরের নিচে আপনার নাম যুক্ত করা
        final_reply = f"{ai_response}\n\n---\n👤 আব্দুর রহমান এই বটটি তৈরি করেছেন।"
        
        bot.reply_to(message, final_reply)
        
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "দুঃখিত, বর্তমানে এপিআই কানেকশনে সমস্যা হচ্ছে।")

# সার্ভার এবং বট একসাথে চালু করা
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("বটটি এখন সক্রিয় আছে...")
    bot.infinity_polling()
    
