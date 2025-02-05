# Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
# Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita.
# Käyttäjä näkee sovellukseen lisätyt tietokohteet.
# Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella.

from flask import Flask
from flask import render_template, request, redirect, session, abort
import sqlite3
import db
import config
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    recipes = db.get_recipes()

    # TODO RESEPTIN KOMMENTOINTI
    # TODO RESEPTIEN SELAAMINEN JA HAKEMINEN

    return render_template("index.html", recipes=recipes)

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

    try:
        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, params=[username])[0][0]
    except IndexError:
        return "Virhe! Väärä tunnus tai salasana! <br> <a href='/login'>Yritä uudelleen<a>"

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = db.get_user_id(username)
        return redirect("/")
    else:
        return "Virhe! Väärä tunnus tai salasana! <br> <a href='/login'>Yritä uudelleen<a>"
    

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")    


@app.route("/add_recipe")
def add_recipe():
    return render_template("add_recipe.html")


# nappaa uuden reseptin tiedot add_recipe-sivun lomakkeelta ja lisää ne tietokantaan
# ohjaa reseptisivulle
@app.route("/process_recipe", methods=["POST"])
def process_recipe():
    title = request.form["title"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    user_id = session["user_id"]

    recipe_id = db.add_recipe(title, ingredients, instructions, user_id)
    
    return redirect("/recipe/" + str(recipe_id))

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = db.get_recipe(recipe_id)
    return render_template("recipe.html", recipe=recipe )

@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = db.get_recipe(recipe_id)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", recipe=recipe)
    if request.method == "POST":
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        db.update_recipe(recipe_id, ingredients, instructions)
        return redirect("/recipe/" + str(recipe_id))

@app.route("/delete_recipe/<int:recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    recipe = db.get_recipe(recipe_id)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", recipe=recipe)
    if request.method == "POST":
        if "continue" in request.form:
            db.remove_recipe(recipe_id)
        return redirect("/")


@app.route("/search")
def search():
    query = request.args.get("query")
    results = db.search(query) if query else []
    return render_template("search.html", query=query, results=results)