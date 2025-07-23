import os
from dotenv import load_dotenv
import stripe

from src.utils.billing import BillingService
from src.affiliate.affiliate_router import apply_affiliate_credit
from src.plan.usage_limiter import is_usage_allowed

# ✅ Load env & Stripe config
load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")
PRICE_ID = os.getenv("STRIPE_PRICE_ID")
print("✅ PRICE_ID loaded:price_1RnO0ZRCUn2IYiUcuINUCz1O", PRICE_ID)

def main():
    email = "user@example.com"
    user_id = "u123"
    plan = "pro"
    referrer = "r001"

    # 🧩 Step 1: Apply affiliate credit
    print(f"💰 Crediting referrer {referrer} for user {user_id}")
    apply_affiliate_credit(user_id, referrer)

    # 🔒 Step 2: Usage limiter check
    if not is_usage_allowed(plan, used_today=2):
        print("🚫 Daily usage limit reached")
        return

    # 🧾 Step 3: Create customer
    billing = BillingService()
    customer_id = billing.create_customer(email=email, user_id=user_id)
    if not customer_id:
        print("❌ Customer creation failed")
        return

    # 💳 Step 4: Attach test payment method
    try:
        payment_method = stripe.PaymentMethod.attach(
            "pm_card_visa",
            customer=customer_id
        )
        stripe.Customer.modify(
            customer_id,
            invoice_settings={"default_payment_method": payment_method.id}
        )
    except Exception as e:
        print("⚠️ Payment method setup failed:", e)
        return

    # 🧾 Step 5: Create subscription
    subscription_id = billing.create_subscription(customer_id)
    if subscription_id:
        print("🎉 Subscription active for user", user_id)
    else:
        print("⚠️ Subscription creation failed")

if __name__ == "__main__":
    main()
