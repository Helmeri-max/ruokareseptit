# Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
# Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita.
# Käyttäjä näkee sovellukseen lisätyt tietokohteet.
# Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella.

from flask import Flask
from flask import render_template, request, redirect, session
import sqlite3
import db
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

@app.route("/")
def index():
    # etusivulle linkit kirjautumiseen ja rekisteröitymiseen

    return render_template("index.html")

# lomakkeet joilla käyttäjä syöttää tiedot
# ohjaa sivulle /create
@app.route("/register")
def register():
    return render_template("register.html")

# nappaa ja käsittelee tiedot /registerin lomakkeelta
# ohjaa kirjautumissivulle jos tunnuksen luonti onnistuu, muuten etusivulle
@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "Virhe! Salasanat eivät täsmää! <a href='/register'>Yritä uudelleen<a>"
    try:
        # tallenna tunnus tietokantaan
        password_hash = generate_password_hash(password1)
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, params=[username, password_hash])
    except sqlite3.IntegrityError:
        return "Virhe! Tunnus on jo käytössä! <a href='/register'>Yritä uudelleen<a>"
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

# nappaa kirjautumistiedot /loginilta, käsittelee ne
# ohjaa etusivulle
@app.route("/process_login", methods=["POST"])
def process_login():
    username = request.form["username"]
    password = request.form["password"]

    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, params=[username])[0][0]

    # temp
    return redirect("/")

#    if check_password_hash(password_hash, password):
#        session["username"] = username
#        return redirect("/")
#    else:
#        return "Virhe! Väärä salasana! <a href='/login'>Yritä uudelleen<a>"
    
   # SECRET KEY YMS SESSION HOITO



