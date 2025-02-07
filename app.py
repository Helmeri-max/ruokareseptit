from flask import Flask
from flask import render_template, request, redirect, session, abort
import sqlite3
import db
from db_operations import get_recipes, get_recipe, get_user_id, remove_recipe, add_recipe, update_recipe, search, add_comment, get_comments
from helper import require_login
import config
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    recipes = get_recipes()
    return render_template("index.html", recipes=recipes)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if len(username) > 100 or not username or len(password1) > 100 or not password1:
        abort(403)

    if password1 != password2:
        return "Virhe! Salasanat eivät täsmää! <a href='/register'>Yritä uudelleen<a>"
    try:
        password_hash = generate_password_hash(password1)
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, params=[username, password_hash])
    except sqlite3.IntegrityError:
        return "Virhe! Tunnus on jo käytössä! <a href='/register'>Yritä uudelleen<a>"
    return redirect("/login")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/process_login", methods=["POST"])
def process_login():
    username = request.form["username"]
    password = request.form["password"]
    if len(username) > 100 or len(password) > 100:
        abort(403)

    try:
        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, params=[username])[0][0]
    except IndexError:
        return "Virhe! Väärä tunnus tai salasana! <br> <a href='/login'>Yritä uudelleen<a>"

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = get_user_id(username)
        return redirect("/")
    else:
        return "Virhe! Väärä tunnus tai salasana! <br> <a href='/login'>Yritä uudelleen<a>"
    

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")    


@app.route("/add_recipe")
def add_recipe_page():
    return render_template("add_recipe.html")


@app.route("/process_recipe", methods=["POST"])
def process_recipe():
    require_login()
    title = request.form["title"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    user_id = session["user_id"]

    if len(title) > 100 or not title or len(ingredients) > 5000 \
    or len(instructions) > 5000:
        abort(403)

    recipe_id = add_recipe(title, ingredients, instructions, user_id)
    
    return redirect("/recipe/" + str(recipe_id))


@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = get_recipe(recipe_id)
    comments = get_comments(recipe_id)
    if not recipe:
        abort(404)
    return render_template("recipe.html", recipe=recipe , comments=comments)


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    require_login()
    recipe = get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", recipe=recipe)
    if request.method == "POST":
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        if len(ingredients) > 5000 or len(instructions) > 5000:
            abort(403)
        update_recipe(recipe_id, ingredients, instructions)
        return redirect("/recipe/" + str(recipe_id))


@app.route("/delete_recipe/<int:recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    require_login()
    recipe = get_recipe(recipe_id)
    if not recipe:
        abort(404)
    if recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", recipe=recipe)
    if request.method == "POST":
        if "continue" in request.form:
            remove_recipe(recipe_id)
        return redirect("/")


@app.route("/search")
def search_page():
    query = request.args.get("query")
    if len(query) > 100:
        abort(403)
    results = search(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/add_comment", methods=["POST"])
def add_comment_page():
    require_login()
    comment_content = request.form["comment"]
    recipe_id = request.form["recipe_id"]
    if not comment_content or not recipe_id or len(comment_content) > 5000:
        abort(403)
    user_id = session["user_id"]
    comment_id = add_comment(user_id, recipe_id, comment_content)
    return redirect("/recipe/" + str(recipe_id))
    




# Kommentoinnin lisäys:
    # kommentin muokkaus-sivu + linkki reseptisivulla
    # kommentin poisto-sivu + linkki reseptisivulla