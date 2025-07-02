from flask import Flask, request
from scraper import scrape_news
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

@app.route('/')
def home():
    return "BPJS News Bot Active!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data.get('message', {}).get('text', '')
    if message == "/refresh":
        scrape_news()
    return "", 200

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_news, 'interval', hours=1)
    scheduler.start()
    app.run(host="0.0.0.0", port=5000)
