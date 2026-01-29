from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Simple code generator model
generator = pipeline(
    "text-generation",
    model="gpt2",
    max_length=200
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    prompt = f"Write a Python script that does the following:\n{user_input}\nCode:\n"
    result = generator(prompt)[0]["generated_text"]

    return jsonify({"reply": result})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)