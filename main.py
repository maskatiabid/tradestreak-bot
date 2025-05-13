import openrouter
import time

# Set your API key here (replace with your actual key)
api_key = "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"  # Your OpenRouter API Key
openrouter.api_key = api_key

# Function to generate a stock tip using OpenRouter
def generate_tip():
    try:
        # Assuming OpenRouter uses the `openrouter.generate()` method for completion
        # Use the correct method for generating text
        response = openrouter.generate(
            prompt="Give me a stock tip for today.",
            max_tokens=100
        )

        if 'choices' in response and len(response['choices']) > 0:
            tip = response['choices'][0]['text']
            return tip
        else:
            return "Error generating tip."

    except Exception as e:
        print(f"Error generating tip: {e}")
        return "Error generating tip."

# Function to post the tip
def post_tip():
    tip = generate_tip()
    if "Error" not in tip:
        print(f"Posting Tip: {tip}")
        # Here you can add your posting logic (e.g., post to a channel, database, etc.)
    else:
        print(tip)

# Simulate scheduled task (runs every minute or as needed)
def scheduler():
    while True:
        print(f"[Scheduler] Time check: {time.strftime('%H:%M')}")
        post_tip()
        time.sleep(60)  # Wait for 1 minute before generating the next tip

# Start the bot
print("[Bot] Starting bot...")
scheduler()  # This will keep the bot running and generating tips periodically
