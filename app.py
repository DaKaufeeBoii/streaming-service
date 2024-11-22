from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_connection():
    con= sqlite3.connect("users.db")
    return con

def create_table():
    con= create_connection()
    cur= con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS newuser(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, username TEXT, password TEXT, number TEXT, email TEXT)''')
    con.commit()
    con.close()
    return redirect("/feedback")

@app.route("/admin")
def admin():
    con=create_connection()
    cur=con.cursor()
    cur.execute('SELECT* FROM newuser')
    data= cur.fetchall()
    return render_template('admin.html', users=data)
    print(data)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        number = request.form.get("number")
        email = request.form.get("email")
        con= create_connection()
        cur= con.cursor()
        cur.execute('''INSERT INTO newuser(number, email) VALUES(?, ?)''', (number, email))
        con.commit()
        cur.close()
        print(f"Received: Number={number}, Email={email}")
        return redirect('/feedback')
    return render_template("login.html")

@app.route("/registration", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name= request.form.get("name")
        surname= request.form.get("surname")
        con= create_connection()
        cur= con.cursor()
        cur.execute('''INSERT INTO newuser(username, password, name, surname) VALUES(?, ?, ?, ?)''', (username, password, name, surname))
        user = cur.fetchone()
        con.commit()
        cur.close()
        print(f"Received: Username={username}, Password={password}, Name={name}, Surname={surname}")
        return redirect('/login')
    return render_template("registration.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

if __name__ == "__main__":
    create_connection()
    create_table()
    app.run(debug=True)