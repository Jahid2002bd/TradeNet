"""
test_billing.py

Tests billing calculation and service usage confirmation.
"""

from src.utils.billing_service import BillingService

def test_calculate_basic_charge():
    service = BillingService()
    amount = 200.0
    charge = service.calculate_charge(amount)
    expected = round(amount * 0.05, 2)
    assert charge == expected

def test_calculate_charge_zero():
    service = BillingService()
    amount = 0.0
    charge = service.calculate_charge(amount)
    assert charge == 0.0

def test_calculate_large_charge():
    service = BillingService()
    amount = 10000.0
    charge = service.calculate_charge(amount)
    expected = round(amount * 0.05, 2)
    assert charge == expected

def test_register_affiliate():
    service = BillingService()
    result = service.register_affiliate("user123", "referral456")
    assert result is True

def test_validate_payment_method():
    service = BillingService()
    assert service.is_supported_method("stripe") is True
    assert service.is_supported_method("unknown_gateway") is False

def test_generate_invoice_message():
    service = BillingService()
    msg = service.generate_invoice("Jahid", 199.99)
    assert "Invoice for Jahid" in msg
    assert "$199.99" in msg
