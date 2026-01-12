import os
from flask import Flask, render_template
from predictor import predict_match

app = Flask(__name__)

@app.route("/")
def home():
    result = predict_match()
    return render_template("index.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
