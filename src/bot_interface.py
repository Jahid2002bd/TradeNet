import time

def send_signal_to_user(signal_data, auto_mode=False):
    """
    Sends signal with reasoning and confidence to user
    :param signal_data: dict from signal_engine
    :param auto_mode: bool toggle
    """

    print("\n📡 TradeNet AI Signal\n--------------------------")
    print(f"🧠 Decision: {signal_data['signal']}")
    print(f"📊 Confidence: {signal_data['confidence']}%")
    print(f"🔍 Reason: {signal_data['reason']}")
    print(f"⚙️ Action: {signal_data['action']}")
    print("--------------------------\n")

    # Manual confirmation (CLI version)
    if not auto_mode and signal_data['signal'] == "BUY":
        user_input = input("🤖 Jahid, trade nibo? (yes/no): ").strip().lower()
        if user_input == "yes":
            print("✅ Trade Confirmed by Jahid. Executing...")
            time.sleep(1)
        else:
            print("🛑 Trade skipped on user request.")

# Placeholder: Telegram integration could be added here with Bot Token