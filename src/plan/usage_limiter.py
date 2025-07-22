# src/plan/usage_limiter.py

PLAN_LIMITS = {
    "free": {"daily_signals": 5},
    "pro": {"daily_signals": 999},
}

def is_usage_allowed(plan: str, used_today: int) -> bool:
    limit = PLAN_LIMITS.get(plan, {}).get("daily_signals", 0)
    return used_today < limit
