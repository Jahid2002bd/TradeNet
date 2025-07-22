from src.data_fusion import fuse_market_data
from src.indicator_engine import analyze_indicators
from src.signal_logger import save_signals
from src.decision_layer import generate_trade_decisions
from src.execution_engine import execute_signals
from src.loophole_finder import detect_loopholes
from src.strategy_refiner import refine_strategy
from src.signal_booster import apply_boosts  # ✅ Stage 9 added

def main():
    # 🟢 Stage 1: Market Snapshot
    snapshot = fuse_market_data()
    print("\n📊 Market Snapshot:")
    for category, assets in snapshot.items():
        if category == "timestamp":
            print(f"🕒 Timestamp: {assets}")
        else:
            print(f"\n📂 {category.upper()} ➤")
            for symbol, data in assets.items():
                print(f"  {symbol}: {data}")

    # 🧠 Stage 2: Signal Generation
    signal_summary = analyze_indicators(snapshot)

    # 🎯 Stage 9: Apply confidence boosts based on learned patterns
    signal_summary = apply_boosts(signal_summary)

    print("\n⚙️ Final Signal Summary (with bonus boost if applicable):")
    for symbol, signal in signal_summary.items():
        msg = f"➤ {symbol}: {signal['signal']} ({signal['confidence']}%)"
        if "note" in signal:
            msg += f" | {signal['note']}"
        print(msg)

    # 📝 Stage 3: Save signal logs
    save_signals(signal_summary)

    # 💬 Stage 4: Human-style decisions
    decisions = generate_trade_decisions(snapshot, signal_summary)
    print("\n📣 Trade Decisions:")
    for symbol, decision in decisions.items():
        print(f"➤ {decision['summary']}")

    # ⚡ Stage 5: Execute if threshold met
    execute_signals(signal_summary, auto_mode=True, threshold=85)

    # 🔍 Stage 7: Pattern detection
    detect_loopholes()

    # 🧠 Stage 8: Refine strategy from past execution
    refine_strategy()

if __name__ == "__main__":
    main()