from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler
import json
import os

TOKEN = os.getenv("BOT_TOKEN")  # token dari Render
app = Flask(__name__)
bot = Bot(token=TOKEN)

# Inisialisasi dispatcher
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

# Load user data
USERDATA_FILE = "userdata.json"
if os.path.exists(USERDATA_FILE):
    with open(USERDATA_FILE, "r") as f:
        user_data = json.load(f)
else:
    user_data = {}

# Command handler
def start(update, context):
    chat_id = str(update.effective_user.id)
    if chat_id not in user_data:
        user_data[chat_id] = {"balance": 0, "last_claim": 0}
        with open(USERDATA_FILE, "w") as f:
            json.dump(user_data, f)
    update.message.reply_text("🦖 Welcome to Dino Hunter Mining!\nType /claim to start mining GBLN!")

def claim(update, context):
    chat_id = str(update.effective_user.id)
    if chat_id not in user_data:
        update.message.reply_text("Ketik /start dulu ya!")
        return
    user_data[chat_id]["balance"] += 10  # mining reward
    with open(USERDATA_FILE, "w") as f:
        json.dump(user_data, f)
    update.message.reply_text(f"✅ Claimed 10 GBLN!\nYour balance: {user_data[chat_id]['balance']} GBLN")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("claim", claim))

# Webhook handler
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"
