from src.utils.money_management import calculate_position_size

def test_calculate_position_size_normal():
    # 1% risk of $10,000 = $100, price diff = $5 → size = 20
    size = calculate_position_size(10000, 0.01, 100.0, 95.0)
    assert size == 20.0

def test_calculate_position_size_zero_diff():
    # Entry and SL are same → size = 0
    size = calculate_position_size(5000, 0.02, 50.0, 50.0)
    assert size == 0.0
