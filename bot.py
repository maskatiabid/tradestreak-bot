import telebot
import json
import os

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # replace this
bot = telebot.TeleBot(BOT_TOKEN)

CHANNEL_LINK = "https://t.me/TradeStreakChannel"
ADMIN_ID = 123456789  # replace this with your Telegram ID

approve_file = "utils/approve_list.json"

# Ensure approve_list.json exists
if not os.path.exists(approve_file):
    with open(approve_file, "w") as f:
        json.dump([], f)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 Welcome to TradeStreak Signals!\n\nWe send 3 expert tips per day on stocks & crypto.")
    bot.send_message(message.chat.id, "📅 Subscription: ₹499/month\n\n✅ To join, send payment via UPI below:")
    bot.send_photo(message.chat.id, open("Abid QR Code.jpg", "rb"))
    bot.send_message(message.chat.id, "📨 After payment, reply here with a screenshot or type 'Paid'. You'll be verified manually.")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    with open(approve_file, "r") as file:
        approved = json.load(file)

    if message.text.lower() in ["paid", "done", "payment done"]:
        bot.send_message(message.chat.id, "🧾 Thank you! Your payment will be manually verified. You'll receive the channel link shortly.")
        bot.send_message(ADMIN_ID, f"👤 {message.from_user.first_name} (@{message.from_user.username}) claims to have paid.\nApprove with:\n`/approve {message.chat.id}`", parse_mode="Markdown")

    elif message.text.startswith("/approve"):
        parts = message.text.split()
        if len(parts) == 2:
            try:
                user_id = int(parts[1])
                if user_id not in approved:
                    approved.append(user_id)
                    with open(approve_file, "w") as f:
                        json.dump(approved, f)
                    bot.send_message(user_id, f"✅ You're approved! Join the channel here: {CHANNEL_LINK}")
                    bot.send_message(message.chat.id, "✅ Approved and sent channel link.")
                else:
                    bot.send_message(message.chat.id, "User already approved.")
            except ValueError:
                bot.send_message(message.chat.id, "Invalid ID.")
        else:
            bot.send_message(message.chat.id, "Usage: /approve USER_ID")

bot.polling()
