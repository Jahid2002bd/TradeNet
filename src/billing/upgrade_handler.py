# src/billing/upgrade_handler.py

import stripe

def upgrade_subscription(sub_id: str, new_price_id: str) -> bool:
    try:
        updated = stripe.Subscription.modify(sub_id, cancel_at_period_end=False, items=[{
            "id": stripe.Subscription.retrieve(sub_id)["items"]["data"][0]["id"],
            "price": new_price_id,
        }])
        print(f"✅ Subscription upgraded: {updated.id}")
        return True
    except Exception as e:
        print(f"⚠️ Upgrade failed: {e}")
        return False
