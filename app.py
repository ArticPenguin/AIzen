from flask import Flask, render_template, request, Response
from flask_cors import CORS
from llm import ask_llm
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    def generate():
        for chunk in ask_llm(data["message"]):
            yield chunk

    return Response(generate(), mimetype="text/plain")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, threaded=True)
