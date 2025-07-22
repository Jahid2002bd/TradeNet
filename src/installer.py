import os

def verify_structure() -> None:
    expected = ["src", "logs", "config", "README.md"]
    for item in expected:
        if not os.path.exists(item):
            print(f"❌ Missing: {item}")
        else:
            print(f"✅ Found: {item}")