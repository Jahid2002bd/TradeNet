# src/affiliate/affiliate_router.py

def apply_affiliate_credit(user_id: str, referrer_code: str) -> bool:
    """
    Credit the referrer if a user signs up with referral code.
    """
    # Save this link in database / cache
    print(f"💰 Crediting referrer {referrer_code} for user {user_id}")
    return True
