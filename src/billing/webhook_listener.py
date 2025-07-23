# src/billing/webhook_listener.py

import os
import stripe
from flask import Flask, request, abort
from dotenv import load_dotenv
from src.user_plan_manager import update_user_plan, deactivate_user, notify_admin

load_dotenv()
app = Flask(__name__)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
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
    customer_id = data.get("customer", "—")
    subscription_id = data.get("id", "—")

    print(f"🔔 Stripe Event: {event_type}")

    if event_type == "invoice.payment_failed":
        print(f"❌ Payment failed → Customer: {customer_id}")
        deactivate_user(customer_id)
        notify_admin(f"Payment failed for {customer_id} → user deactivated")

    elif event_type == "customer.subscription.deleted":
        print(f"🟥 Subscription cancelled → {subscription_id}")
        deactivate_user(customer_id)
        notify_admin(f"Subscription cancelled → {customer_id} downgraded")

    elif event_type == "customer.subscription.updated":
        plan_name = data.get("items", {}).get("data", [{}])[0].get("price", {}).get("nickname", "unknown")
        print(f"🔄 Subscription updated → Plan: {plan_name}")
        update_user_plan(customer_id, plan_name)
        notify_admin(f"Plan updated → {customer_id} now on {plan_name}")

    else:
        print(f"⚠️ Unhandled event: {event_type}")

    return "", 200
