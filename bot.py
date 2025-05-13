import os
import openai
import logging
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, Update, JobQueue
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
channel_id = os.getenv("CHANNEL_ID")

# Initialize Telegram Bot
bot = Bot(token=telegram_bot_token)

# Setup logging to help identify errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Type /get_tip to get a stock tip.")

# Function to get a stock tip using OpenAI
def get_tip(update: Update, context: CallbackContext):
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

# Function to send tip automatically
def send_automatic_tip(context: CallbackContext):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Give me a short stock market tip.",
            temperature=0.7,
            max_tokens=60
        )
        tip = response.choices[0].text.strip()
        bot.send_message(chat_id=channel_id, text=f"Stock Tip: {tip}")
    except Exception as e:
        logger.error(f"Error while sending automatic tip: {str(e)}")

# Setup the job scheduler
def schedule_jobs(updater: Updater):
    job_queue = updater.job_queue
    scheduler = BackgroundScheduler()
    
    # Scheduling the automatic tip every 8 hours (you can change this interval)
    scheduler.add_job(send_automatic_tip, IntervalTrigger(hours=8), args=[updater])
    
    # Start the scheduler
    scheduler.start()

# Setup the command handlers
def main():
    updater = Updater(token=telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher
    
    # Add command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('get_tip', get_tip))
    
    # Schedule the automatic tips
    schedule_jobs(updater)
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
