from flask import Flask, request, render_template
from flask import jsonify

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/api/my_json", methods=["GET", "POST"])
def my_json():
    if request.method == "POST":
        data = {"text": "Hello, AdaBrain", "user": "It's me Ada"}

        return jsonify(data)
    return "200"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
