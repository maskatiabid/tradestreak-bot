import os
import openai
import telegram
from datetime import datetime
import time

# Load your API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

openai.api_key = OPENAI_API_KEY
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def generate_signal(asset_type="crypto"):
    prompt = f"Generate a trading signal for a trending {asset_type} with the following format:\n" \
             "Asset:\nAction:\nEntry Price:\nTarget Price:\nStop Loss:\nBrief (1 line explanation):"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating {asset_type} signal: {str(e)}"

def post_signal():
    crypto_signal = generate_signal("crypto")
    stock_signal = generate_signal("stock")

    bot.send_message(chat_id=CHANNEL_ID, text=f"🚨 *Crypto Signal*\n{crypto_signal}", parse_mode="Markdown")
    bot.send_message(chat_id=CHANNEL_ID, text=f"📈 *Stock Signal*\n{stock_signal}", parse_mode="Markdown")

if __name__ == "__main__":
    while True:
        now = datetime.now()
        if now.hour in [9, 13, 17]:
            post_signal()
            time.sleep(3600)
        else:
            time.sleep(600)
