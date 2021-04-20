import requests
from flask import Flask, json, request, render_template
from flask import jsonify, redirect, url_for
from pymongo import MongoClient
from bson import json_util
from pymongo.database import Database
from pymongo.periodic_executor import PeriodicExecutor

app = Flask(__name__)
app.secret_key = "hello"

client = MongoClient(
    "mongodb://admin:FGCxns24841@node12656-shopping.app.ruk-com.cloud:11007"
)
mydb = client["Shopping"]
stock = mydb["Stock"]
user = mydb["User"]


@app.route("/")
def hello_world():
    Data = 0
    Product = []
    Name = []
    price = []
    IMG = []
    for post in stock.find():
        Product.append(post["ID_Product"])
        Name.append([post["Name"]])
        price.append(post["Price"])
        IMG.append(post["ID_Product"] + ".jpg")
    return render_template(
        "index.html", Data=Data, Product=Product, Name=Name, Price=price, IMG=IMG
    )


@app.route("/index", methods=["GET", "POST"])
def index():
    ID = int(request.args.get("Data"))
    print(ID)
    Product = []
    Name = []
    price = []
    IMG = []
    for post in stock.find():
        Product.append(post["ID_Product"])
        Name.append([post["Name"]])
        price.append(post["Price"])
        IMG.append(post["ID_Product"] + ".jpg")
    return render_template(
        "index.html", Data=ID, Product=Product, Name=Name, Price=price, IMG=IMG
    )


# @app.route("/main/api")
# def main():
#     Data = request.args.get("Data")
#     if check == 0:
#         redirect(url_for("register"))
#     return render_template("index.html")


# @app.route("/api/my_json", methods=["GET", "POST"])
# def my_json():
#     if request.method == "POST":
#         data = {"text": "Hello, AdaBrain", "user": "It's me Ada"}

#         return jsonify(data)
#     return "200"


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
                post["IDUser"],
                post["username"],
                post["password"],
                post["name"],
                post["surname"],
                post["phone"],
                post["email"],
                post["address"],
            }
        )
    return json_util.dumps(output)


# insert function api POST
@app.route("/api/insertstock", methods=["GET", "POST"])
def insertstock():
    ID_Product = request.form["ID_Product"]
    Amount = request.form["Amount"]
    Name = request.form["Name"]
    Price = request.form["Price"]
    Description = request.form["Description"]
    Data = {
        "ID_Product": ID_Product,
        "Amount": Amount,
        "Price": Price,
        "Name": Name,
        "Description": Description,
    }
    stock.insert_one(Data)
    return jsonify({"status": "Create Success"})


@app.route("/api/insertuser", methods=["GET", "POST"])
def insertuser():
    username = request.form["username"]
    password = request.form["password"]
    name = request.form["Name"]
    surname = request.form["surname"]
    phone = request.form["phone"]
    email = request.form["email"]
    address = request.form["address"]
    credit = 0
    if user.count() == 0:
        print(0)
        IDUser = 1
    else:
        num = user.find({"username": username}).count()
        if num >= 1:
            return redirect(url_for("register"))
        else:
            print(1)
            IDUser = user.count() + 1
    Data = {
        "IDUser": IDUser,
        "username": username,
        "password": password,
        "name": name,
        "surname": surname,
        "phone": phone,
        "email": email,
        "address": address,
        "credit": credit,
    }
    output = ""
    user.insert_one(Data)
    for post in user.find({"username": username}):
        output.append({post["IDUser"]})
    return redirect(url_for("check", Data=IDUser))


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


# Login
@app.route("/api/login", methods=["GET", "POST"])
def login():
    Username = request.form["Username"]
    Password = request.form["Password"]
    num = user.find({"username": Username, "password": Password}).count()
    Data = 0
    if num == 1:
        for post in user.find({"username": Username}):
            Data = post["IDUser"]
        return redirect(url_for("check", Data=Data))
    else:
        return render_template("register.html")


@app.route("/register")
def register():
    return render_template("register.html", Data=0)


@app.route("/cart", methods=["GET", "POST"])
def cart():
    ID = int(request.args.get("Data"))
    mycol = mydb[str(ID)]
    mycart = []
    check = []
    Datacrat = []
    Price = []
    IMG = []
    Pricesum = []
    status = []
    choice = 0
    sum = 0
    if int(mycol.find().count()) >= 1:
        choice = choice + 1
        for post in mycol.find():
            for nameproduct in stock.find({"ID_Product": post["ProductID"]}):
                Datacrat.append(nameproduct["Name"])
                Price.append(nameproduct["Price"])
                mycart.append(post["ProductID"])
                check.append(post["QTY"])
                IMG.append(post["ProductID"] + ".jpg")
                Pricesum.append(int(post["QTY"]) * int(nameproduct["Price"]))
                sum = sum + (int(post["QTY"]) * int(nameproduct["Price"]))
                status.append(post["Status"])
        return render_template(
            "cart.html",
            Datacrat=Datacrat,
            Price=Price,
            mycart=mycart,
            check=check,
            ID=ID,
            Pricesum=Pricesum,
            sum=sum,
            IMG=IMG,
            choice=choice,
            status=status,
        )
    else:
        choice = choice + 2
        return render_template(
            "cart.html",
            Datacrat=Datacrat,
            Price=Price,
            mycart=mycart,
            check=check,
            ID=ID,
            Pricesum=Pricesum,
            sum=sum,
            IMG=IMG,
            choice=choice,
            status=status,
        )


@app.route("/api/insertcart", methods=["GET", "POST"])
def insertcart():
    ID = int(request.form["Data"])
    DataProduct = request.form["DataProduct"]
    QTY = request.form["QTY"]
    mycol = mydb[str(ID)]
    if ID != 0:
        check = int(mycol.find({"ProductID": DataProduct}).count())
        if check == 1:
            Pluscart = []
            Checkcart = []
            for post in mycol.find({"ProductID": DataProduct}):
                for get in stock.find({"ID_Product": DataProduct}):
                    if int(get["Amount"]) < (int(post["QTY"]) + int(QTY)):
                        Pluscart.append(get["Amount"])
                    else:
                        Pluscart.append(int(post["QTY"]) + int(QTY))
            Update = {"ProductID": DataProduct}
            newvalues = {"$set": {"QTY": int(Pluscart[0])}}
            if mycol.update_one(Update, newvalues):
                print(check)
                return redirect(url_for("cart", Data=ID))
        else:
            for get in stock.find({"ID_Product": DataProduct}):
                if int(get["Amount"]) < int(QTY):
                    data = {
                        "ProductID": DataProduct,
                        "QTY": get["Amount"],
                        "Status": "limit",
                    }
                else:
                    data = {
                        "ProductID": DataProduct,
                        "QTY": QTY,
                        "Status": "Normarl",
                    }
            if mycol.insert_one(data):
                Pluscart = []
                for post in mycol.find({"ProductID": DataProduct}):
                    for get in stock.find({"ID_Product": DataProduct}):
                        if int(get["Amount"]) < (int(post["QTY"])):
                            Pluscart.append(get["Amount"])
                            Update = {"ProductID": DataProduct}
                            newvalues = {"$set": {"QTY": int(Pluscart[0])}}
                            if mycol.update_one(Update, newvalues):
                                return redirect(url_for("cart", Data=ID))
                        else:
                            return redirect(url_for("cart", Data=ID))
    else:
        return render_template("register.html", Data=0)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    ID = int(request.args.get("Data"))
    mycol = mydb[str(ID)]
    mycart = []
    check = []
    Datacrat = []
    Price = []
    IMG = []
    Pricesum = []
    status = []
    choice = 0
    sum = 0
    if int(mycol.find().count()) >= 1:
        choice = choice + 1
        for post in mycol.find():
            for nameproduct in stock.find({"ID_Product": post["ProductID"]}):
                Datacrat.append(nameproduct["Name"])
                Price.append(nameproduct["Price"])
                mycart.append(post["ProductID"])
                check.append(post["QTY"])
                IMG.append(post["ProductID"] + ".jpg")
                Pricesum.append(int(post["QTY"]) * int(nameproduct["Price"]))
                sum = sum + (int(post["QTY"]) * int(nameproduct["Price"]))
                status.append(post["Status"])
        return render_template(
            "checkout.html",
            Datacrat=Datacrat,
            Price=Price,
            mycart=mycart,
            check=check,
            ID=ID,
            Pricesum=Pricesum,
            sum=sum,
            IMG=IMG,
            choice=choice,
            status=status,
        )


@app.route("/api/delcart", methods=["GET", "POST"])
def delcart():
    ID = int(request.args.get("Data"))
    ID_P = request.args.get("DataP")
    mycol = mydb[str(ID)]
    Delete = {"ProductID": ID_P}
    mycol.find_one_and_delete(Delete)
    return render_template("cart.html", ID=ID)


@app.route("/product_detail")
def prod_detail():
    ID = int(request.args.get("Data"))
    ID_P = request.args.get("DataP")
    response = requests.get("https://covid19.th-stat.com/api/open/today")
    dataurl = response.json()
    data = [dataurl["Confirmed"], dataurl["NewConfirmed"], dataurl["Recovered"]]
    DataProduct = []
    if ID != 0:
        for post in stock.find({"ID_Product": ID_P}):
            DataProduct.append(post["ID_Product"])
            DataProduct.append(post["Name"])
            DataProduct.append(post["ID_Product"] + ".jpg")
            DataProduct.append(post["Price"])
            DataProduct.append(post["Amount"])
            DataProduct.append(post["Description"])
        return render_template(
            "product_detail.html", DataProduct=DataProduct, ID=ID, data=data
        )
    else:
        return render_template("register.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/products")
def prods():
    return render_template("products.html")


@app.route("/check", methods=["GET", "POST"])
def check():
    ID = int(request.args.get("Data"))
    if ID != 0:
        Dataa = []
        DataC = []
        main = []
        for post in user.find({"IDUser": ID}):
            Dataa.append([post["username"]])
            Dataa.append([post["password"]])
            Dataa.append([post["name"]])
            Dataa.append([post["surname"]])
            Dataa.append([post["phone"]])
            Dataa.append([post["email"]])
            Dataa.append([post["address"]])
        for post in user.find({"IDUser": ID}):
            main.append(["Username"])
            main.append(["Password"])
            main.append(["Name"])
            main.append(["Surname"])
            main.append(["Phone"])
            main.append(["Email"])
            main.append(["Address"])
        for a in user.find({"IDUser": ID}):
            DataC.append([a["IDUser"]])
            DataC.append([a["username"]])
            DataC.append([a["credit"]])
        return render_template("myaccount.html", Data=Dataa, DataC=DataC, main=main)


@app.route("/myaccount", methods=["GET", "POST"])
def myaccount():
    Data = request.args.get("Dataa")
    print(Data.username)
    return render_template("myaccount.html", Data=Data)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)
