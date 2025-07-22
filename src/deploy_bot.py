import time
import traceback
from run_bot import run_bot

def deploy_loop(interval_sec: int = 600) -> None:
    print("🛠️ Empire Deployment Loop Started.")

    while True:
        try:
            print("\n🔁 Empire Bot cycle begins...")
            run_bot()
            print(f"⏳ Sleeping for {interval_sec} seconds...\n")
            time.sleep(interval_sec)

        except KeyboardInterrupt:
            print("🛑 Deployment halted by user.")
            break

        except (ValueError, RuntimeError) as e:
            print(f"⚠️ Known error → {type(e).__name__}: {e}")
            time.sleep(10)

        except Exception as e:
            print(f"❌ Unknown error → {type(e).__name__}: {e}")
            traceback.print_exc()
            time.sleep(10)

if __name__ == "__main__":
    deploy_loop()