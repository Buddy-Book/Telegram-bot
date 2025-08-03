from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN", "your_token_here")

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

STATE = {"active": False}

def start(update, context):
    update.message.reply_text("Welcome! Send 1 to start, 2 to stop.")
    STATE["active"] = False

def one(update, context):
    STATE["active"] = True
    update.message.reply_text("✅ Betting simulation started.")

def two(update, context):
    STATE["active"] = False
    update.message.reply_text("⛔ Betting simulation stopped.")

def simulate(update, context):
    if not STATE["active"]:
        update.message.reply_text("Bot inactive. Send 1 to activate.")
        return

    msg = update.message.text.lower()
    if "six" in msg or "boundary" in msg:
        update.message.reply_text("📉 Boundary detected → Lay bet triggered")
    elif "wicket" in msg:
        update.message.reply_text("📈 Wicket detected → Back bet triggered")
    else:
        update.message.reply_text("No trigger.")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.regex("^1$"), one))
dispatcher.add_handler(MessageHandler(Filters.regex("^2$"), two))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, simulate))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot is live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
