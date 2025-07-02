from flask import Flask, request
from telegram import Update
from telegram.ext import Application, Dispatcher, CommandHandler, ContextTypes
from telegram_bot import handle_update  # Fungsi handler Anda

import os
import config

app = Flask(__name__)

@app.route(f"/{config.TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.create_task(handle_update(update, ContextTypes.DEFAULT_TYPE))
    return "OK"

if __name__ == "__main__":
    # Inisialisasi Application
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()

    # Set Webhook URL
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{config.TELEGRAM_TOKEN}"
    application.bot.set_webhook(url=webhook_url)

    print("✅ Webhook set to:", webhook_url)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
