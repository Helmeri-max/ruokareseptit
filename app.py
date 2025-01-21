from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    db = sqlite3.connect("database.db")
    db.execute("INSERT INTO syotteet (testisyote) VALUES ('kikkeli')")
    db.commit()
    result = db.execute("SELECT count(*) FROM syotteet").fetchone()
    
    return "Tähän etusivu"

@app.route("/testilomake")
def testilomake():

