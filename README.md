# 🧠 TradeNet_AI — AI-Powered Modular Trading System

TradeNet_AI is a professional-grade, cross-market automated trading bot featuring signal fusion, institutional booster layers, outcome memory, Telegram/Web control panels, and self-learning pattern logic.

---

## 🚀 Core Features

- ✅ Signal generation & approval engine
- ✅ Booster stacking: PatternBoost, InstBoost, OutcomeBoost
- ✅ Auto-learning loop using pattern memory
- ✅ DRY-RUN vs LIVE toggle system
- ✅ Execution tracking & outcome logging
- ✅ Web Dashboard (Flask API)
- ✅ Telegram Bot Control with multilingual support
- ✅ Modular, PyCharm-ready codebase with clean structure

---

## 📁 Folder Structure

```bash
TradeNet_AI/
├── .venv/                        # Python virtual environment
├── logs/
│   └── Empire/
│       └── config/
│           ├── global_config.json
│           ├── execution_log.json
│           ├── pattern_memory.json
│           ├── signal_log.json
│           └── trade_log.json
├── src/
│   └── utils/
│       ├── fetcher/
│       │   ├── commodity.py
│       │   ├── crypto.py
│       │   ├── forex.py
│       │   └── stock.py
│       ├── approval_engine.py
│       ├── auto_trader.py
│       ├── bot_interface.py
│       ├── config_loader.py
│       ├── dashboard.py
│       ├── data_fetcher.py
│       ├── data_fusion.py
│       ├── db_handler.py
│       ├── decision_layer.py
│       ├── deploy_bot.py
│       ├── execution_engine.py
│       ├── execution_logger.py
│       ├── indicator_engine.py
│       ├── indicators.py
│       ├── installer.py
│       ├── institution_booster.py
│       ├── loophole_finder.py
│       ├── main.py
│       ├── outcome_tracker.py
│       ├── pattern_booster.py
│       ├── pattern_finder.py
│       ├── pattern_learner.py
│       ├── pattern_memory.py
│       ├── run_bot.py
│       ├── sentiment_analysis.py
│       ├── signal_booster.py
│       ├── signal_engine.py
│       ├── signal_logger.py
│       ├── strategy_refiner.py
│       ├── summary_bot.py
│       ├── telegram_bot.py
│       ├── telegram_controller.py
│       ├── trade_approval.py
│       └── trade_executor.py
├── requirements.txt
├── README.md
