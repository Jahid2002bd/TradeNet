import os

required_keys = [
    "STRIPE_SECRET_KEY",
    "STRIPE_WEBHOOK_SECRET",
    "STRIPE_CHECKOUT_URL"
]

missing = [key for key in required_keys if not os.getenv(key)]

if missing:
    print("❌ নিচের ENV key গুলো মিসিং — config ভুল হলে SaaS চলবে না:")
    for key in missing:
        print(f"→ {key}")
else:
    print("✅ সকল environment key ঠিক আছে — deploy safe.")
