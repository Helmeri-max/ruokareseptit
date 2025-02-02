import sqlite3
from flask import g

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def last_insert_id():
    return g.last_insert_id    
    
def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result


def get_recipes():
    sql = """SELECT recipe_id, r.title, count(m.comment_id) comments_total, MAX(m.sent_at) last_comment_at
             FROM recipes r
             LEFT JOIN comments m USING(recipe_id)
             GROUP BY 1,2 ORDER BY 1 DESC"""
    return query(sql)


def add_recipe(title, ingredients, instructions, user_id):
    sql = """INSERT INTO recipes (title, ingredients, instructions, user_id, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))"""
    execute(sql, [title, ingredients, instructions, user_id])
    recipe_id = last_insert_id()
    return recipe_id


def get_user_id(username):
    sql = """SELECT user_id FROM users where username = ?"""
    user_id = query(sql, params=[username])[0][0]
    return user_id

def get_recipe(recipe_id):
    sql = """SELECT recipe_id, title, ingredients, instructions, user_id
            FROM recipes 
            WHERE recipe_id = ?"""
    recipe = query(sql, params=[recipe_id])
    return recipe[0]

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE recipe_id = ?"
    execute(sql, params=[recipe_id])

def update_recipe(recipe_id, ingredients, instructions):
    sql = "UPDATE recipes SET ingredients = ?, instructions = ? WHERE recipe_id = ?"
    execute(sql, params=[ingredients, instructions, recipe_id])