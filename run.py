import os
import sys
from dotenv import load_dotenv
import stripe
from flask import Flask, render_template

from src.utils.billing import BillingService
from src.affiliate.affiliate_router import apply_affiliate_credit
from src.plan.usage_limiter import is_usage_allowed

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return "✅ TradeNet server is running!"

def run_onboarding():
    load_dotenv()
    stripe_key = os.getenv("STRIPE_API_KEY")
    stripe_price = os.getenv("STRIPE_PRICE_ID")

    if not stripe_key or not stripe_price:
        print("❌ Missing STRIPE_API_KEY or STRIPE_PRICE_ID in .env")
        sys.exit(1)

    stripe.api_key = stripe_key
    print(f"✅ Stripe configured → Price ID: {stripe_price}")

    # Example user inputs
    email = "user@example.com"
    user_id = "u123"
    plan = "pro"
    referrer_code = "r001"

    print(f"🎁 Crediting affiliate {referrer_code} for user {user_id}")
    apply_affiliate_credit(user_id=user_id, referrer_code=referrer_code)

    if not is_usage_allowed(plan=plan, used_today=2):
        print("🚫 Usage limit reached")
        return
    print("✅ Usage allowed")

    billing = BillingService()

    print("🧾 Creating Stripe customer...")
    cid = billing.create_customer(email=email, user_id=user_id)
    if not cid:
        print("❌ Customer creation failed")
        return
    print(f"✅ Customer created → {cid}")

    print("💳 Attaching pm_card_visa…")
    try:
        pm = stripe.PaymentMethod.attach("pm_card_visa", customer=cid)
        stripe.Customer.modify(
            cid,
            invoice_settings={"default_payment_method": pm.id}
        )
        print(f"✅ Payment method → {pm.id}")
    except Exception as e:
        print(f"⚠️ Payment setup failed: {e}")
        return

    print("📦 Creating subscription…")
    sub = billing.create_subscription(cid)
    if sub and hasattr(sub, "id"):
        print(f"🎉 Subscription active → {sub.id}")
    else:
        print("⚠️ Subscription creation failed")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "onboard":
        run_onboarding()
    else:
        try:
            from waitress import serve
            serve(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
        except ImportError:
            app.run(host="0.0.0.0", port=8000, debug=True)
