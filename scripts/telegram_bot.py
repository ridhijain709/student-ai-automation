import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import requests

# Configuration
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
BACKEND_URL = "http://localhost:3000"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    sender = update.message.from_user.username or "unknown"
    
    # Call backend
    try:
        response = requests.post(f"{BACKEND_URL}/telegram/analyze", json={
            "sender": sender,
            "raw_text": text
        })
        
        if response.status_code == 200:
            data = response.json()
            reply = f"Summary: {data['summary']}\n\nDraft Reply: {data['draft_reply']}"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Error processing message.")
    except Exception as e:
        logging.error(f"Error calling backend: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Service unavailable.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handle all text messages
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)
    
    application.run_polling()
