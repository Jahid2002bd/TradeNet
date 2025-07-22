from config_loader import load_config
from signal_engine import generate_signals
from approval_engine import approve_signals
from signal_booster import boost_signals
from pattern_booster import boost_with_patterns
from institution_booster import boost_institutional_behavior
from trade_executor import send_order
from outcome_tracker import track_outcome
from pattern_learner_old import learn_pattern_from_execution

def run_bot() -> None:
    print("🚀 Empire Bot launching...")

    config = load_config()
    dry_mode = config.get("dry_run", True)

    # Step 1: Generate signals
    signals = generate_signals()

    # Step 2: Approve signals
    approved = approve_signals(signals)

    # Step 3: Boost by outcome
    boosted = boost_signals(approved)

    # Step 4: Boost by pattern memory
    patterned = boost_with_patterns(boosted)

    # Step 5: Boost by institutional behavior
    inst_boosted = boost_institutional_behavior(patterned)

    # Step 6: Execute trades + Track outcome
    executed_trades = {}
    for symbol, trade in inst_boosted.items():
        trade["mode"] = "DRY-RUN" if dry_mode else "LIVE"
        send_order(trade, dry_run=dry_mode)

        # Simulated outcome logic (replace with real result later)
        result = "win" if trade["signal"] == "BUY" and trade["confidence"] >= 85 else "loss"
        track_outcome(symbol, result, trade)
        executed_trades[symbol] = trade

    # Step 7: Learn from executed trades
    learn_pattern_from_execution(executed_trades)

    print("✅ Empire Bot cycle complete.")

if __name__ == "__main__":
    run_bot()