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