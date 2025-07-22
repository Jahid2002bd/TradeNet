from flask import Flask, render_template, jsonify, request, redirect, session
import datetime

app = Flask(__name__)
app.secret_key = "tradenet_secret_key"  # For session management

# Sample signal data (replace later with real engine or DB)
signals = [
    {
        "symbol": "BTCUSDT",
        "signal": "Buy",
        "confidence": "High",
        "booster": "RSI Oversold",
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    },
    {
        "symbol": "ETHUSDT",
        "signal": "Sell",
        "confidence": "Medium",
        "booster": "MACD Divergence",
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    },
    {
        "symbol": "XAUUSD",
        "signal": "Buy",
        "confidence": "High",
        "booster": "Breakout Level",
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }
]

@app.route("/")
def homepage():
    return render_template("tradenet_home.html")

@app.route("/generate")
def generate_signals():
    return jsonify(signals)

@app.route("/signal/<symbol>")
def signal_detail(symbol):
    signal_info = next((s for s in signals if s["symbol"] == symbol), None)
    if signal_info:
        return render_template("signal_detail.html", **signal_info)
    else:
        return f"No data found for {symbol}", 404

@app.route("/ai_explain/<symbol>")
def ai_explain(symbol):
    signal_info = next((s for s in signals if s["symbol"] == symbol), None)
    if not signal_info:
        return "No signal found", 404

    # Tactical explanation block — AI logic can be added here
    explanation = f"{symbol} shows a {signal_info['signal']} signal with {signal_info['confidence']} confidence due to {signal_info['booster']}. This pattern typically suggests a tactical entry or exit based on market momentum or reversal indicators."
    return explanation

@app.route("/income")
def income_dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("income_dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        if user == "admin" and pw == "1234":
            session["user"] = user
            return redirect("/")
        else:
            return "Login failed", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
