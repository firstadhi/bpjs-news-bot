from flask import Flask, request
from telegram_bot import handle_update
from scraper import schedule_scraping
import config

app = Flask(__name__)

@app.route('/')
def index():
    return 'BPJS Ketenagakerjaan News Bot is running.'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    handle_update(update)
    return 'OK', 200

if __name__ == '__main__':
    schedule_scraping()
    app.run(host='0.0.0.0', port=5000)
