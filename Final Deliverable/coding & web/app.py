from flask import Flask, render_template, request, redirect, url_for, session 
import datetime as dt
import ibm_db
conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=sqm48729;PWD=Grn9XBDhpYjTAZiW",'','')

app =Flask(__name__)

@app.route("/")

def home():
    return render_template("home.html")

@app.route("/account")

def account():
    return render_template("index.html")

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
        sql = "SELECT * FROM nutrition_database WHERE name =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, food)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            return render_template('index.html', msg="You are already a member, please login using your details")
        else:
            insert_sql = "INSERT INTO nutrition_database VALUES (?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, food)
            ibm_db.bind_param(prep_stmt, 2, quantity)
            ibm_db.bind_param(prep_stmt, 3, protein)
            ibm_db.bind_param(prep_stmt, 4, carbohydrate)
            ibm_db.bind_param(prep_stmt, 5, fat)
            ibm_db.execute(prep_stmt)
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
    return render_template("database.csv")

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
        sql = "SELECT * FROM students WHERE name =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            return render_template('index.html', msg="You are already a member, please login using your details")
        else:
            insert_sql = "INSERT INTO students VALUES (?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, age)
            ibm_db.bind_param(prep_stmt, 3, address)
            ibm_db.bind_param(prep_stmt, 5, contact)
            ibm_db.bind_param(prep_stmt, 6, mail)
            ibm_db.bind_param(prep_stmt, 7, password)
            ibm_db.bind_param(prep_stmt, 8, confirm_password)
            ibm_db.execute(prep_stmt)
            date=dt.datetime.now()
            f=open("database.txt","a")
            f.write(f"\n{date}\n")
            f.write(f" name:{name}\n age:{age}\n address:{address}\n contact:{contact}\n mail:{mail}\n password:{password}\n confirm_password:{confirm_password}\n\n\n")
            return render_template("result.html", msg="Student Data saved successfuly..",name=name,age=age,address=address,contact=contact,mail=mail,password=password,confirm_password=confirm_password)

if __name__=='__main__':
    app.run(debug=True)