# src/billing/webhook_listener.py

import json
import stripe
from flask import Flask, request, abort

app = Flask(__name__)
stripe.api_key = os.getenv("STRIPE_API_KEY", "")

# Replace with your actual webhook secret from Stripe Dashboard
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        abort(400)

    event_type = event["type"]
    data = event["data"]["object"]
    print(f"🔔 Event: {event_type}")

    if event_type == "invoice.payment_failed":
        print(f"❌ Payment failed for customer: {data.get('customer')}")
    elif event_type == "customer.subscription.deleted":
        print(f"🟥 Subscription cancelled: {data.get('id')}")
    elif event_type == "customer.subscription.updated":
        print(f"🔄 Subscription updated: {data.get('id')}")

    return "", 200
