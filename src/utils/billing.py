# src/utils/billing.py

import os
import stripe
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# 🔐 Read credentials from .env
stripe.api_key = os.getenv("STRIPE_API_KEY")
PRICE_ID = os.getenv("STRIPE_PRICE_ID")

class BillingService:
    def __init__(self):
        if not stripe.api_key or not PRICE_ID:
            raise ValueError("⚠️ Missing STRIPE_API_KEY or STRIPE_PRICE_ID in .env")

    @staticmethod
    def create_customer(email: str, user_id: str) -> str:
        try:
            customer = stripe.Customer.create(
                email=email,
                metadata={"user_id": user_id}
            )
            print(f"▶ Creating customer...\nCustomer ID: {customer.id}")
            return customer.id
        except Exception as e:
            print(f"[BillingService] Error creating customer: {e}")
            return ""

    @staticmethod
    def create_subscription(customer_id: str) -> str:
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": PRICE_ID}],
            )
            print(f"▶ Creating subscription...\nSubscription ID: {subscription.id}")
            return subscription.id
        except Exception as e:
            print(f"[BillingService] Error creating subscription: {e}")
            return ""
