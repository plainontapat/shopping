import bson
from flask import Flask, json, request, render_template
from flask import jsonify
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)

client = MongoClient(
    "mongodb://admin:FGCxns24841@node12656-shopping.app.ruk-com.cloud:11007"
)
mydb = client["Shopping"]
stock = mydb["Stock"]
user = mydb["User"]


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/api/my_json", methods=["GET", "POST"])
def my_json():
    if request.method == "POST":
        data = {"text": "Hello, AdaBrain", "user": "It's me Ada"}

        return jsonify(data)
    return "200"


@app.route("/get_all", methods=["GET", "POST"])
def get_all():
    output = []
    for post in mydb.TestMongoNew.find():
        output.append({post["author"], post["Phone"]})
    return json_util.dumps(output)


@app.route("/api/get_user", methods=["GET", "POST"])
def get_user():
    output = []
    for post in user.find():
        output.append(
            {
                post["ID"],
                post["Username"],
                post["Credit"],
                post["Name"],
                post["Phone"],
                post["Email"],
            }
        )
    return json_util.dumps(output)


# insert function api POST
@app.route("/api/insertstock", methods=["GET", "POST"])
def insertstock():
    ID_Product = request.form["ID_Product"]
    Amount = request.form["Amount"]
    Name = request.form["Name"]
    Description = request.form["Description"]
    Data = {
        "ID_Product": ID_Product,
        "Amount": Amount,
        "Name": Name,
        "Description": Description,
    }
    stock.insert_one(Data)
    return jsonify({"status": "Create Success"})


@app.route("/api/insertuser", methods=["GET", "POST"])
def insertuser():
    ID_User = request.form["ID_User"]
    Description = request.form["Description"]
    Status = request.form["Status"]
    Credit = request.form["Credit"]
    Data = {
        "ID_Product": ID_User,
        "Description": Description,
        "Status": Status,
        "Credit": Credit,
    }
    user.insert_one(Data)
    return jsonify({"status": "insert Success"})


# Get Delete
@app.route("/api/Deletestock", methods=["GET", "POST"])
def Delete():
    ID_Product = request.form["ID_Product"]
    Delete = {"ID_Product": ID_Product}
    stock.find_one_and_delete(Delete)
    return jsonify({"status": "Delete success"})


# # Get Update
@app.route("/api/Updatestock", methods=["GET", "POST"])
def Update():
    ID_Product = request.form["ID_Product"]
    Amount = request.form["Amount"]
    Name = request.form["Name"]
    Description = request.form["Description"]
    Update = {"ID_Product": ID_Product}
    newvalues = {"$set": {"Amount": Amount, "Name": Name, "Description": Description}}
    stock.update_one(Update, newvalues)
    return jsonify({"status": "Update Success"})


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


@app.route("/myaccount")
def base():
    return render_template("myaccount.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
