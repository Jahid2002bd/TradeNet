from flask import Flask, jsonify, request
from signal_engine import generate_signals
from approval_engine import approve_signals
from execution_engine import execute_signals
from outcome_tracker import get_summary  # optional summary logic

app: Flask = Flask(__name__)


@app.route("/", methods=["GET"])
def home() -> tuple:
    return jsonify({"status": "Empire Dashboard Online"}), 200


@app.route("/generate", methods=["GET"])
def generate() -> tuple:
    try:
        signals = generate_signals()
        approved = approve_signals(signals)
        return jsonify({"approved_signals": approved}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/execute", methods=["POST"])
def execute() -> tuple:
    try:
        payload = request.get_json(force=True)  # accepts raw signal batch
        if not isinstance(payload, dict):
            raise ValueError("Invalid payload format. Expected dict of signals.")

        execute_signals(payload)
        return jsonify({"status": "Signals executed"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/summary", methods=["GET"])
def summary() -> tuple:
    try:
        result = get_summary()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status() -> tuple:
    return jsonify({
        "bot": "ready",
        "approved": True,
        "routes": ["/generate", "/execute", "/summary", "/status"],
        "version": "v1.0.3"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
