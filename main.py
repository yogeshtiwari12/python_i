from flask import Flask, request
import json
import os
import requests
import time
import threading

app = Flask(__name__)

# Get Discord webhook from environment variables
DISCORD_WEBHOOK_URL = os.environ.get('dc_webhook')


@app.route("/", methods=["GET"])
def home():
    return "PayPal Webhook Listener is Running!"

@app.route("/paypal-webhook", methods=["POST"])
def paypal_webhook():
    data = request.json

    if data.get("event_type") == "PAYMENT.CAPTURE.COMPLETED":
        resource = data.get("resource", {})
        payer_email = resource.get("payer", {}).get("email_address", "Unknown")
        amount = resource.get("amount", {}).get("value", "0.00")
        currency = resource.get("amount", {}).get("currency_code", "USD")

        embed = {
            "title": "💰 **Payment Received!**",
            "description": f"**Amount:** {amount} {currency}\n**From:** {payer_email}",
            "color": 5814783,  # You can customize the color
            "footer": {
                "text": "Payment Status"
            }
        }
        
        # message = f"💰 **Payment Received!**\n**Amount:** {amount} {currency}\n**From:** {payer_email}"

        # Send message to Discord
        # headers = {"Content-Type": "application/json"}
        # response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, headers=headers)

        response = requests.post(
            DISCORD_WEBHOOK_URL, 
            json={"embeds": [embed]},
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 204:
            print(f"Failed to send message to Discord: {response.text}")

    return "OK", 200

def keep_alive():
    while True:
        try:
            requests.get("https://d963f1be-b764-4d6e-ae37-792afe1a24db-00-1lrzsn37c8b9r.kirk.replit.dev/")
            print("Self-ping successful")
        except Exception as e:
            print(f"Self-ping failed: {e}")
        time.sleep(600)  # Ping every 10 minutes

# Start keep-alive in a background thread
threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
