# generate a bunch of content to test the app with large amounts of data

import random
import string
import sqlite3


db = sqlite3.connect("database.db")


db.execute("DELETE FROM users")
db.execute("DELETE FROM recipes")
db.execute("DELETE FROM comments")
db.execute("DELETE FROM recipe_tags")


user_count = 1000
recipe_count = 10**5
comment_count = 10**6


def random_string(length):
    result = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return result

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
            ["user" + str(i)])

for i in range(1, recipe_count + 1):

    sql = "INSERT INTO recipes (title, ingredients, instructions, user_id, created_at) VALUES (?,?,?,?,datetime('now'))"

    db.execute(sql, ["recipe" + str(i), random_string(200), random_string(200), random.randint(1, user_count)])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    recipe_id = random.randint(1, recipe_count)
    sql = """INSERT INTO comments (comment_content, sent_at, user_id, recipe_id)
                VALUES (?, datetime('now'), ?, ?)"""
    db.execute(sql, ["message" + str(i), user_id, recipe_id])

db.commit()
db.close()