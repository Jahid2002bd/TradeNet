import stripe
import os
from dotenv import load_dotenv

load_dotenv()  # ✅ this loads .env file

# ✅ this sets the API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# check if key loaded
if not stripe.api_key:
    print("❌ STRIPE_SECRET_KEY missing or not loaded")
    exit()

session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    mode="subscription",
    line_items=[
        {
            "price": "price_1RnO0ZRCUn2IYiUcuINUCz1O",   # ← Replace with your actual Price ID
            "quantity": 1
        }
    ],
    success_url="https://yourdomain.com/success",
    cancel_url="https://yourdomain.com/cancel"
)

print(f"✅ Checkout URL:\n{session.url}")
