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


@app.route("/register")
def regiter():
    return render_template("register.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/product_detail")
def prod_detail():
    return render_template("product_detail.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/products")
def prods():
    return render_template("products.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
