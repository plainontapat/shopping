import requests
from flask import Flask, json, request, render_template
from flask import jsonify, redirect, url_for, session
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
app.secret_key = "hello"

client = MongoClient(
    "mongodb://admin:FGCxns24841@node12656-shopping.app.ruk-com.cloud:27017"
)
mydb = client["Shopping"]
stock = mydb["Stock"]
user = mydb["User"]
His = mydb["History"]
response = requests.get("https://covid19.th-stat.com/api/open/today")
dataurl = response.json()
data = [dataurl["Confirmed"], dataurl["NewConfirmed"], dataurl["Recovered"]]


@app.route("/")
def hello_world():
    Data = 0
    credit = 0
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
        "index.html",
        Data=Data,
        Product=Product,
        Name=Name,
        Price=price,
        IMG=IMG,
        credit=credit,
    )


@app.route("/index", methods=["GET", "POST"])
def index():
    if "user" in session:
        ID = session["user"]
        Product = []
        Name = []
        price = []
        IMG = []
        if session["search"] != "":
            for post in stock.find({"Name": session["search"]}):
                Product.append(post["ID_Product"])
                Name.append([post["Name"]])
                price.append(post["Price"])
                IMG.append(post["ID_Product"] + ".jpg")
            session["search"] = ""
        elif session["Brand"] != "":
            for post in stock.find({"Brand": session["Brand"]}):
                Product.append(post["ID_Product"])
                Name.append([post["Name"]])
                price.append(post["Price"])
                IMG.append(post["ID_Product"] + ".jpg")
            session["Brand"] = ""
        else:
            for post in stock.find():
                Product.append(post["ID_Product"])
                Name.append([post["Name"]])
                price.append(post["Price"])
                IMG.append(post["ID_Product"] + ".jpg")
        return render_template(
            "index.html",
            Data=ID,
            Product=Product,
            Name=Name,
            Price=price,
            IMG=IMG,
        )
    else:
        return redirect(url_for("register"))


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
    return redirect(url_for("check"))


@app.route("/api/Updateuser", methods=["GET", "POST"])
def Updateuser():
    ID = session["user"]
    if ID != 0:
        print(ID)
        username = request.form["Username"]
        password = request.form["Password"]
        name = request.form["Name"]
        surname = request.form["Surname"]
        phone = request.form["Phone"]
        email = request.form["Email"]
        address = request.form["Address"]
        Update = {"IDUser": ID}
        newvalues = {
            "$set": {
                "username": username,
                "password": password,
                "name": name,
                "surname": surname,
                "phone": phone,
                "email": email,
                "address": address,
            }
        }
        if user.update_one(Update, newvalues):
            return redirect(url_for("check"))
        else:
            return redirect(url_for("check"))
    else:
        return redirect(url_for("check"))


@app.route("/api/cradit", methods=["GET", "POST"])
def credit():
    ID = request.form["IDUser"]
    username = request.form["username"]
    credit = request.form["credit"]
    print(credit, ID, username)
    for post in user.find({"username": username}):
        creditnew = int(post["credit"]) + int(credit)
    Update = {"username": username}
    newvalues = {
        "$set": {
            "credit": creditnew,
        }
    }
    if user.update_one(Update, newvalues):
        session["credit"] = creditnew
        return redirect(url_for("check"))
    else:
        return redirect(url_for("index", Data=0))


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
    if num == 1:
        for post in user.find({"username": Username}):
            session["user"] = post["IDUser"]
            session["credit"] = post["credit"]
        return redirect(url_for("check"))
    else:
        return redirect(url_for("register"))


@app.route("/register")
def register():
    return render_template("register.html", Data=0)


@app.route("/cart", methods=["GET", "POST"])
def cart():
    if "user" in session:
        ID = session["user"]
        credit = session["credit"]
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
                    if int(nameproduct["Amount"]) > int(post["QTY"]):
                        Pricesum.append(int(post["QTY"]) * int(nameproduct["Price"]))
                        sum = sum + (int(post["QTY"]) * int(nameproduct["Price"]))
                        status.append("Normal")
                    elif int(nameproduct["Amount"]) == int(post["QTY"]):
                        Pricesum.append(int(post["QTY"]) * int(nameproduct["Price"]))
                        sum = sum + (int(post["QTY"]) * int(nameproduct["Price"]))
                        status.append("limit")
                    else:
                        Pricesum.append(0)
                        choice = 0
                        status.append("without")
            session["sum"] = sum
            return render_template(
                "cart.html",
                Datacrat=Datacrat,
                Price=Price,
                mycart=mycart,
                check=check,
                ID=ID,
                Pricesum=Pricesum,
                IMG=IMG,
                choice=choice,
                credit=credit,
                status=status,
                data=data,
            )
        else:
            choice = choice + 1
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
                credit=credit,
                status=status,
                data=data,
            )
    else:
        return redirect(url_for("register"))


@app.route("/api/insertcart", methods=["GET", "POST"])
def insertcart():
    ID = session["user"]
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
                return redirect(url_for("cart"))
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
                                return redirect(url_for("cart"))
                        else:
                            return redirect(url_for("cart"))
    else:
        return render_template("register.html", Data=0)


@app.route("/api/delcart", methods=["GET", "POST"])
def delcart():
    ID = session["user"]
    credit = session["credit"]
    ID_P = request.args.get("DataP")
    mycol = mydb[str(ID)]
    Delete = {"ProductID": ID_P}
    mycol.find_one_and_delete(Delete)
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "user" in session:
        ID = session["user"]
        mycart = []
        check = []
        Datacrat = []
        Price = []
        IMG = []
        Pricesum = []
        Bill = []
        for post in His.find({"IDUser": ID}):
            for nameproduct in stock.find({"ID_Product": post["ID_Product"]}):
                Bill.append(post["ID_His"])
                Datacrat.append(nameproduct["Name"])
                Price.append(nameproduct["Price"])
                mycart.append(post["ID_Product"])
                check.append(post["QTY"])
                IMG.append(post["ID_Product"] + ".jpg")
                Pricesum.append(int(post["QTY"]) * int(nameproduct["Price"]))
        return render_template(
            "checkout.html",
            Datacrat=Datacrat,
            Price=Price,
            mycart=mycart,
            check=check,
            ID=ID,
            Pricesum=Pricesum,
            IMG=IMG,
            Bill=Bill,
        )
    else:
        return redirect(url_for("register"))


@app.route("/product_detail")
def prod_detail():
    if "user" in session:
        ID = session["user"]
        credit = session["credit"]
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
                "product_detail.html",
                DataProduct=DataProduct,
                ID=ID,
                data=data,
                credit=credit,
            )
        else:
            return redirect(url_for("register"))
    else:
        return redirect(url_for("register"))


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/products")
def prods():
    return render_template("products.html")


@app.route("/check", methods=["GET", "POST"])
def check():
    if "user" in session:
        ID = session["user"]
        credit = session["credit"]
        session["search"] = ""
        session["Brand"] = ""
        session["sum"] = 0
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
            return render_template(
                "myaccount.html", Data=Dataa, DataC=DataC, main=main, credit=credit
            )
    else:
        return redirect(url_for("register"))


# confirm API
@app.route("/api/confirm", methods=["GET", "POST"])
def confirm():
    ID = session["user"]
    roud = int(His.find().count())
    if roud == 0:
        number = int(His.find().count()) + 1
    else:
        for bill in His.find():
            number = int(bill["ID_His"]) + 1
    Hisnumber = int(number)
    mycol = mydb[str(ID)]
    sum = session["sum"]
    credit = session["credit"]
    summit = credit - sum
    print(summit)
    QTY = 0
    if summit >= 0:
        print(1)
        for i in mycol.find():
            print(2)
            for post in stock.find({"ID_Product": i["ProductID"]}):
                print(int(post["Amount"]))
                if int(post["Amount"]) >= int(i["QTY"]):
                    print(4)
                    QTY = int(post["Amount"]) - int(i["QTY"])
                    Update = {"ID_Product": i["ProductID"]}
                    newvalues = {"$set": {"Amount": QTY}}
                    stock.update_one(Update, newvalues)
                    Data = {
                        "ID_His": Hisnumber,
                        "ID_Product": i["ProductID"],
                        "IDUser": ID,
                        "QTY": int(i["QTY"]),
                    }
                    His.insert_one(Data)
                    Delete = {"ProductID": i["ProductID"]}
                    mycol.find_one_and_delete(Delete)
                else:
                    return redirect(url_for("cart"))
        Updateuser = {"IDUser": ID}
        newvaluesuser = {"$set": {"credit": summit}}
        if user.update_one(Updateuser, newvaluesuser):
            print(5)
            session["credit"] = summit
            session["sum"] = 0
            return redirect(url_for("checkout"))
        else:
            return redirect(url_for("cart"))
    else:
        return redirect(url_for("index"))


@app.route("/myaccount", methods=["GET", "POST"])
def myaccount():
    return render_template("myaccount.html")


@app.route("/api/search", methods=["GET", "POST"])
def search():
    if session["user"] == "":
        return redirect(url_for("register"))
    else:
        session["search"] = request.form["Name"]
        return redirect(url_for("index"))


@app.route("/api/type", methods=["GET", "POST"])
def Type():
    if session["user"] == "":
        return redirect(url_for("register"))
    else:
        typeproduct = request.args.get("type")
        session["Brand"] = typeproduct
        return redirect(url_for("index"))


@app.route("/api/logout", methods=["GET", "POST"])
def logout():
    session.pop("user", None)
    session.pop("credit", None)
    session.pop("sum", None)
    session.pop("Brand", None)
    session.pop("search", None)
    return redirect(url_for("hello_world"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
