# src/utils/chatbot_ui.py

"""
chatbot_ui.py

Provides a simple CLI for user to chat with the trading assistant.
"""

from src.utils.ai_explain_core import generate_explanation


def start_chat() -> None:
    """
    Starts the chat loop for user to ask about signals or risk.
    """
    print("Welcome to TradeNet AI Assistant. Type 'exit' to quit.")
    while True:
        user_input_str = input("You: ").strip()
        if user_input_str.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        response_str = handle_user_query(user_input_str)
        print(f"Assistant: {response_str}")


def handle_user_query(query: str) -> str:
    """
    Parses user query and returns assistant response.

    Expected format:
      explain SYMBOL ENTRY SL TP [RR]
    """
    tokens = query.split()
    if len(tokens) >= 5 and tokens[0].lower() == "explain":
        symbol_str = tokens[1]
        try:
            entry_val = float(tokens[2])
            sl_val = float(tokens[3])
            tp_val = float(tokens[4])
            rr_val = float(tokens[5]) if len(tokens) > 5 else None
        except ValueError:
            return "Invalid numbers. Use: explain SYMBOL ENTRY SL TP [RR]"

        return generate_explanation(
            symbol=symbol_str,
            entry_price=entry_val,
            stop_loss_price=sl_val,
            take_profit_price=tp_val,
            rr_ratio=rr_val
        )

    return "Use command: explain SYMBOL ENTRY SL TP [RR]"


if __name__ == "__main__":
    start_chat()
