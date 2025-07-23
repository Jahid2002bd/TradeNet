from src.data_fusion import fuse_market_data
from src.indicator_engine import analyze_indicators
from src.signal_booster import apply_boosts
from src.signal_logger import save_signals
from src.decision_layer import generate_trade_decisions
from src.execution_engine import execute_signals
from src.loophole_finder import detect_loopholes
from src.strategy_refiner import refine_strategy

def main() -> None:
    # 🟢 Stage 1: Market Snapshot
    snapshot = fuse_market_data()
    print("\n📊 Market Snapshot:")
    for category, assets in snapshot.items():
        if category == "timestamp":
            print(f"🕒 Timestamp: {assets}")
            continue
        print(f"\n📂 {category.upper()} ➤")
        for symbol, data in assets.items():
            print(f"  {symbol}: {data}")

    # 🧠 Stage 2: Signal Generation
    signal_summary = analyze_indicators(snapshot)

    # 🎯 Stage 9: Confidence Boost
    boosted_signals = apply_boosts(signal_summary)

    # ⚙️ Display Boosted Signals
    print("\n⚙️ Final Signal Summary:")
    for symbol, signal in boosted_signals.items():
        message = f"➤ {symbol}: {signal['signal']} ({signal['confidence']}%)"
        note = signal.get("note")
        if note:
            message += f" | {note}"
        print(message)

    # 📝 Stage 3: Save Logs
    save_signals(boosted_signals)

    # 💬 Stage 4: Trade Decisions
    decisions = generate_trade_decisions(snapshot, boosted_signals)
    print("\n📣 Trade Decisions:")
    for symbol, decision in decisions.items():
        print(f"➤ {decision['summary']}")

    # ⚡ Stage 5: Execute Signals
    execute_signals(boosted_signals,)

    # 🔍 Stage 7: Detect Loopholes
    detect_loopholes()

    # 🧠 Stage 8: Refine Strategy
    refine_strategy()

if __name__ == "__main__":
    main()
