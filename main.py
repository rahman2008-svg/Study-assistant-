import os
import telebot
from groq import Groq

# আপনার দেওয়া টোকেন এবং এপিআই কি সরাসরি এখানে দেওয়া হলো
# তবে প্রোডাকশনে এগুলো Environment Variable হিসেবে রাখা ভালো
BOT_TOKEN = "8223615159:AAHmqJY28w4t7J-kEf5GB_LNthUWJ0IpXBU"
GROQ_API_KEY = "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"

# বট এবং গ্রক ক্লায়েন্ট সেটআপ
bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! আমি গ্রক এআই চালিত আপনার টেলিগ্রাম বট। আমাকে যেকোনো প্রশ্ন করুন।")

# মেসেজ হ্যান্ডলার (ব্যবহারকারীর বার্তার উত্তর দেওয়া)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Groq API এর মাধ্যমে চ্যাট কমপ্লিশন তৈরি
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message.text,
                }
            ],
            model="llama3-8b-8192", # আপনি চাইলে এখানে অন্য মডেল ব্যবহার করতে পারেন
        )
        
        # এআই এর উত্তরটি বের করে আনা
        ai_reply = chat_completion.choices[0].message.content
        bot.reply_to(message, ai_reply)
        
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "দুঃখিত, বর্তমানে আমার সিস্টেমে সমস্যা হচ্ছে। কিছুক্ষণ পর চেষ্টা করুন।")

# বট চালানো
print("বটটি এখন চালু আছে...")
bot.infinity_polling()

