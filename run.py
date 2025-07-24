#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
import stripe
from flask import Flask, render_template

from src.utils.billing import BillingService
from src.affiliate.affiliate_router import apply_affiliate_credit
from src.plan.usage_limiter import is_usage_allowed

# ————————————— Flask Server Setup ——————————————
app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return "✅ TradeNet server is running!"

# ————————————— CLI Onboarding Runner ——————————————
def run_onboarding():
    load_dotenv()

    stripe_key   = os.getenv("STRIPE_API_KEY")
    stripe_price = os.getenv("STRIPE_PRICE_ID")
    if not stripe_key or not stripe_price:
        print("❌ Missing STRIPE_API_KEY or STRIPE_PRICE_ID in .env")
        sys.exit(1)

    stripe.api_key = stripe_key
    print(f"✅ Stripe configured → Price ID:price_1RnO0ZRCUn2IYiUcuINUCz1O{stripe_price}")


    # Demo user & plan data
    email    = "user@example.com"
    user_id  = "u123"
    plan     = "pro"
    referrer = "r001"

    # 1️⃣ Apply affiliate credit
    print(f"🎁 Crediting affiliate '{referrer}' for user '{user_id}'")
    apply_affiliate_credit(user_id, referrer)

    # 2️⃣ Usage limiter check
    if not is_usage_allowed(plan, used_today=2):
        print("🚫 Usage limit reached")
        return
    print("✅ Usage allowed")

    # 3️⃣ Create Stripe customer
    billing = BillingService()
    print("🧾 Creating Stripe customer...")
    customer_id = billing.create_customer(email, user_id)
    if not customer_id:
        print("❌ Customer creation failed")
        return
    print(f"✅ Customer created → {customer_id}")

    # 4️⃣ Attach test payment method
    print("💳 Attaching payment method `pm_card_visa`…")
    try:
        pm_obj = stripe.PaymentMethod.attach("pm_card_visa", customer=customer_id)
        pm_id  = getattr(pm_obj, "id", pm_obj.get("id"))
        stripe.Customer.modify(
            customer_id,
            invoice_settings={"default_payment_method": pm_id}
        )
        print(f"✅ Payment method attached → {pm_id}")
    except Exception as e:
        print("⚠️ Payment method setup failed:", e)
        return

    # 5️⃣ Create subscription
    print("📦 Creating subscription…")
    subscription_id = billing.create_subscription(customer_id)
    if subscription_id:
        print(f"🎉 Subscription active → {subscription_id}")
    else:
        print("⚠️ Subscription creation failed")

# ————————————— Entry Point ——————————————
if __name__ == "__main__":
    # if invoked with "onboard", run the CLI flow
    if len(sys.argv) > 1 and sys.argv[1] == "onboard":
        run_onboarding()
    else:
        # otherwise launch the server
        try:
            from waitress import serve
            print("🔧 Launching server via Waitress/Gunicorn…")
            serve(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
        except ImportError:
            print("⚠️ Waitress not found. Running Flask built-in server…")
            app.run(host="0.0.0.0", port=8000, debug=True)
