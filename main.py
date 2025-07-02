import requests
import config

def set_webhook():
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/setWebhook"
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{config.TELEGRAM_TOKEN}"
    response = requests.post(url, json={"url": webhook_url})
    print("Webhook response:", response.text)

if __name__ == "__main__":
    set_webhook()
