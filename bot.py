import os
import openai
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
channel_id = os.getenv("CHANNEL_ID")

# Initialize Telegram Bot
bot = Bot(token=telegram_bot_token)

# Function to handle the /start command
def start(update, context):
    update.message.reply_text("Welcome! Type /get_tip to get a stock tip.")

# Function to get a stock tip using OpenAI
def get_tip(update, context):
    try:
        # Request stock tip from OpenAI (this is an example, you can modify the prompt as needed)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Give me a short stock market tip.",
            temperature=0.7,
            max_tokens=60
        )
        tip = response.choices[0].text.strip()
        update.message.reply_text(f"Stock Tip: {tip}")
        
        # Optionally, send the tip to your Telegram channel as well
        bot.send_message(chat_id=channel_id, text=f"Stock Tip: {tip}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

# Setup the command handlers
def main():
    updater = Updater(token=telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher
    
    # Add command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('get_tip', get_tip))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
