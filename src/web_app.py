from pathlib import Path

from flask import Flask, jsonify, render_template, request

from agent_core import AlyssaAgent


app_dir = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(app_dir / "templates"), static_folder=str(app_dir / "static"))
agent = AlyssaAgent()


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    if not question:
        return jsonify({"error": "Question is required."}), 400

    try:
        answer, retrieved_sections = agent.answer(question)
    except Exception as exc:
        return jsonify({"error": f"Agent error: {exc}"}), 500

    return jsonify({"answer": answer, "retrieved_sections": retrieved_sections})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
