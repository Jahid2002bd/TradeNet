#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
import stripe
from flask import Flask, render_template

from src.utils.billing import BillingService
from src.affiliate.affiliate_router import apply_affiliate_credit
from src.plan.usage_limiter import is_usage_allowed

# Flask server setup
app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return "✅ TradeNet server is running!"

# CLI onboarding runner
def run_onboarding():
    load_dotenv()
    key   = os.getenv("STRIPE_API_KEY")
    price = os.getenv("STRIPE_PRICE_ID")
    if not key or not price:
        print("❌ Missing STRIPE_API_KEY or STRIPE_PRICE_ID in .env")
        sys.exit(1)

    stripe.api_key = key
    print(f"✅ Stripe ready → Price ID:price_1RnO0ZRCUn2IYiUcuINUCz1O {price}")

    # Demo data
    email, user_id, plan, referrer = (
        "user@example.com", "u123", "pro", "r001"
    )

    # 1) Affiliate credit
    print(f"🎁 Crediting affiliate {referrer} for user {user_id}")
    apply_affiliate_credit(user_id, referrer)

    # 2) Usage limiter
    if not is_usage_allowed(plan, used_today=2):
        print("🚫 Usage limit reached")
        return
    print("✅ Usage allowed")

    # 3) Create Stripe customer
    billing = BillingService()
    print("🧾 Creating Stripe customer...")
    cid = billing.create_customer(email, user_id)
    if not cid:
        print("❌ Customer creation failed")
        return
    print(f"✅ Customer → {cid}")

    # 4) Attach payment method
    print("💳 Attaching test card pm_card_visa…")
    try:
        pm = stripe.PaymentMethod.attach("pm_card_visa", customer=cid)
        pid = getattr(pm, "id", pm.get("id"))
        stripe.Customer.modify(cid, invoice_settings={"default_payment_method": pid})
        print(f"✅ PM attached → {pid}")
    except Exception as e:
        print("⚠️ Payment failed:", e)
        return

    # 5) Create subscription
    print("📦 Creating subscription…")
    sub = billing.create_subscription(cid)
    sid = getattr(sub, "id", sub)
    if sid:
        print(f"🎉 Subscription active → {sid}")
    else:
        print("⚠️ Subscription failed")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "onboard":
        run_onboarding()
    else:
        try:
            from waitress import serve
            print("🔧 Launching server…")
            serve(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
        except ImportError:
            app.run(host="0.0.0.0", port=8000, debug=True)
