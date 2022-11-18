from flask import Flask, render_template, request, redirect, url_for, session 
import datetime as dt
import json
from nutrients import Calculator
import ibm_db
# conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=sqm48729;PWD=Grn9XBDhpYjTAZiW",'','')

app =Flask(__name__)


@app.route("/")

def home():
    return render_template("home.html")

@app.route("/account")

def account():
    return render_template("create_account.html")

@app.route("/home_page")

def home_page():
    return render_template("home.html")

@app.route("/update")

def update():
    return render_template("update.html")

@app.route("/nutrition_page")

def nutrition_page():
    return render_template("nutrition_assistant.html")

@app.route("/food")

def food():
    return render_template("food.html") 

@app.route("/send",methods=["POST","GET"])

def send():
    if request.method=="POST":  
        food=request.form["food"]
        quantity=request.form["quantity"]
        protein=request.form["protein"]
        carbohydrate=request.form["carbohydrate"]
        fat=request.form["fat"]
        date=dt.datetime.now() 
        f=open("nutrition_database.txt","a")
        f.write(f"\n{date}\n")
        f.write(f" food:{food}\n quantity:{quantity}\n protein:{protein}\n carbohydrate:{carbohydrate}\n fat:{fat}\n\n\n")
        return render_template("nutrition-form.html",food=food,quantity=quantity,protein=protein,carbohydrade=carbohydrate,fat=fat)
                        
@app.route("/views")

def views():
    return render_template("nutrition_database.txt")


@app.route("/food_diet")

def food_diet():
    return render_template("food_diet.html")


@app.route("/view_profile")

def view_profile():
    return render_template("database.txt")

@app.route("/login")

def login():
     return render_template("login.html")
 
@app.route("/about")

def about():
     return render_template("about.html")
 
@app.route("/food_nutrition")

def food_nutrition():
    return render_template("food_nutrition.html")

@app.route("/carrot")

def carrot():
    return render_template("carrot.html")

@app.route("/potato")

def potato():
    return render_template("potato.html")

@app.route("/beans")

def beans():
    return render_template("beans.html")


@app.route("/spinach")

def spinach():
    return render_template("spinach.html")


@app.route("/drumsticks")

def drumsticks():
    return render_template("drumstick.html")


@app.route("/chicken")

def chicken():
    return render_template("chicken.html")


@app.route("/mutton")

def mutton():
    return render_template("mutton.html")


@app.route("/fish")

def fish():
    return render_template("fish.html")


@app.route("/pork")

def pork():
    return render_template("pork.html")

@app.route("/apple")

def apple():
    return render_template("apple.html")


@app.route("/orange")

def orange():
    return render_template("orange.html")


@app.route("/pineapple")

def pineapple():
    return render_template("pineapple.html")

@app.route("/watermelon")

def watermelon():
    return render_template("watermelon.html")

@app.route("/grape")

def grape():
    return render_template("grape.html")

@app.route("/cashews")

def cashews():
    return render_template("cashews.html")

@app.route("/walnuts")

def walnuts():
    return render_template("walnuts.html")

@app.route("/almonds")

def almonds():
    return render_template("almonds.html")

@app.route("/peanuts")

def peanuts():
    return render_template("peanuts.html")

@app.route("/register",methods=["POST","GET"])

def register():
    if request.method=="POST":
        name=request.form["name"]
        age=request.form["age"]
        address=request.form["address"]
        contact=request.form["contact"]
        mail=request.form["mail"]
        password=request.form["password"]
        confirm_password=request.form["confirm_password"]
        date=dt.datetime.now()
        f=open("database.txt","a")
        f.write(f"\n{date}\n")
        f.write(f" name:{name}\n age:{age}\n address:{address}\n contact:{contact}\n mail:{mail}\n password:{password}\n confirm_password:{confirm_password}\n\n\n")
        return render_template("result_result.html", msg="Student Data saved successfuly..",name=name,age=age,address=address,contact=contact,mail=mail,password=password,confirm_password=confirm_password)



app.config["UPLOAD_FOLDER"] = "static/images"

sizes = {}
nutrients = []
responses = []

with open("foods.json", "r") as f:
    foods = json.load(f)


with open("order.txt", "r") as f:
    order = f.read().splitlines(keepends=False)


for i in foods:
    for j in list(i["nuts"].keys()):
        if j not in nutrients:
            nutrients.append(j)
            sizes[j] = i["nuts"][j]["unit"]
    i["image"] = i["name"].replace(" ", "") + ".jpg"
for i in nutrients:
    if i not in order:
        order.append(i)

nutrients = [i for i in order if i in nutrients]


def response_to_list(r):
    buf = []
    new = {}
    for i in r.keys():
        try:
            new[int(i)] = r[i]
        except ValueError:
            pass
    for i in new.keys():
        while i >= len(buf):
            buf.append(0)
        buf[i] = int(new[i])
    return buf

@app.route("/index")
def index():
    return render_template("index.html", tags=nutrients, sizes=sizes, foods=foods)


@app.route("/data", methods=["POST", "GET"])
def data():
    global responses
    form_data = json.loads(request.form["values"])
    prios = json.loads(request.form["prios"])
    prios = response_to_list(prios)
    to_except = json.loads(request.form["except"])
    if len(responses) > 60:
        responses = []
    key = len(responses)
    nuts = response_to_list(form_data)
    if len(nuts) < 1:
        return "INVALID"

    print("LOAD")
    calc = Calculator()
    calc.load_foods(foods, prios, order)
    print("LOADED")
    res = calc.calculate(nuts, except_foods=to_except)
    if len(res["foods"]) == 0:
        return str(-1)
    responses.append(res)
    query = [(i[0], i[1] - 1) for i in zip(nutrients, nuts) if i[1] != 0]
    responses[key]["query"] = query

    return str(key)


@app.route("/result", methods=["GET"])
def result():
    global responses
    data = request.args
    if int(data["id"]) == -1:
        return render_template("noresult.html")
    try:
        resp = responses[int(data["id"])]
    except (ValueError, IndexError):
        return redirect(url_for("index"))
    foods = resp["foods"]
    for j in foods:
        j["nuts"] = {}
        j["qtty"] = len([i for i in foods if i["id"] == j["id"]]) * 10  # TODO: serving size related
    foods = [i for n, i in enumerate(foods) if i not in foods[n + 1 :]]
    return render_template(
        "result.html",
        nuts=list(zip(nutrients, resp["nutrients"])),
        sizes=sizes,
        foods=foods,
        query=resp["query"],
        time=resp["time"],
        likeness=resp["likeness"],
    )

if __name__=='__main__':
    app.run(debug=True)
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=False, use_reloader=True, host="0.0.0.0", port=5000)