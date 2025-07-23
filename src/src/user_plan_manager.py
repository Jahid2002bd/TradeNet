# src/user_plan_manager.py

def update_user_plan(customer_id: str, plan_name: str) -> None:
    print(f"✅ Updating plan for {customer_id} → {plan_name}")
    # TODO: Update your DB or config file
    # Example: db.update_plan(customer_id, plan_name)

def deactivate_user(customer_id: str) -> None:
    print(f"🛑 Deactivating user: {customer_id}")
    # TODO: Block access, revoke tokens, mark inactive
    # Example: db.set_user_status(customer_id, active=False)

def notify_admin(message: str) -> None:
    print(f"📣 ADMIN ALERT → {message}")
    # TODO: Email, Slack, or dashboard log
    # Example: email.send("admin@yourdomain.com", message)
