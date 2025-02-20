# FUNCTIONS THAT OPERATE THE DATABASE IN THIS WEBAPP
import db

def get_recipes(page, page_size):
    sql = """SELECT recipe_id, r.title, count(m.comment_id) comments_total, 
            MAX(m.sent_at) last_comment_at
            FROM recipes r
            LEFT JOIN comments m USING(recipe_id)
            GROUP BY 1,2 ORDER BY 1 DESC
            LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    result = db.query(sql, params=[limit, offset])
    return  result if result else None

def add_recipe(title, ingredients, instructions, user_id, tags):
    sql = """INSERT INTO recipes (title, ingredients, instructions, user_id, created_at)
            VALUES (?, ?, ?, ?, datetime('now'))"""
    db.execute(sql, [title, ingredients, instructions, user_id])
    recipe_id = db.last_insert_id()
    for tag in tags:
        sql = "INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)"
        db.execute(sql, params=[recipe_id, int(tag)])
    return recipe_id

def get_user_id(username):
    sql = """SELECT user_id FROM users where username = ?"""
    user_id = db.query(sql, params=[username])[0][0]
    return user_id

def get_recipe(recipe_id):
    sql = """SELECT recipe_id, title, ingredients, instructions, user_id, username, created_at, recipe_image
            FROM recipes 
            LEFT JOIN users USING(user_id)
            LEFT JOIN recipe_images USING(recipe_id)
            WHERE recipe_id = ?"""
    recipe = db.query(sql, params=[recipe_id])
    return recipe[0] if recipe else None

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE recipe_id = ?"
    db.execute(sql, params=[recipe_id])

def update_recipe(recipe_id, ingredients, instructions):
    sql = "UPDATE recipes SET ingredients = ?, instructions = ? WHERE recipe_id = ?"
    db.execute(sql, params=[ingredients, instructions, recipe_id])

def search(word):
    sql = """SELECT recipe_id, title, ingredients, instructions
            FROM recipes
            WHERE title LIKE ?
            OR ingredients LIKE ?
            OR instructions LIKE ?"""
    term = "%" + word + "%"
    return db.query(sql, params=[term, term, term])

def add_comment(user_id, recipe_id, comment_content):
    sql = """INSERT INTO comments (user_id, recipe_id, comment_content, sent_at)
            VALUES (?, ?, ?, datetime('now'))"""
    db.execute(sql, params=[user_id, recipe_id, comment_content])
    comment_id = db.last_insert_id()
    return comment_id

def get_comments(recipe_id):
    sql = """SELECT username, user_id, comment_id, comment_content, sent_at
            FROM comments 
            LEFT JOIN users USING(user_id)
            WHERE recipe_id = ?
            ORDER BY 5
            """
    return db.query(sql, params=[recipe_id])

def get_comment(comment_id):
    sql = """SELECT username, user_id, comment_id, recipe_id, comment_content, sent_at
            FROM comments
            LEFT JOIN users USING(user_id)
            WHERE comment_id = ?"""
    comment = db.query(sql, params=[comment_id])
    return comment[0] if comment else None

def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE comment_id = ?"
    db.execute(sql, params=[comment_id])

def edit_comment(comment_content, comment_id):
    sql = "UPDATE comments SET comment_content = ? WHERE comment_id = ?"
    db.execute(sql, params=[comment_content, comment_id])

def get_user(user_id):
    sql = """SELECT username, users.user_id, COUNT(distinct recipe_id) as recipe_count,
            COUNT(distinct comment_id) as comment_count
            FROM users
            LEFT JOIN recipes USING(user_id)
            LEFT JOIN comments USING(recipe_id)
            WHERE users.user_id = ?"""
    result = db.query(sql, params=[user_id])
    return result[0] if result else None

def get_users_recipes(user_id, page, page_size):
    sql = """SELECT recipe_id, title
            FROM recipes
            WHERE recipes.user_id = ?
            LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    result = db.query(sql, params=[user_id, limit, offset])
    return result if result else None

def get_recipe_tags(recipe_id):
    sql = """SELECT tag_name
            FROM recipe_tags
            INNER JOIN tags USING(tag_id)
            WHERE recipe_id = ?"""
    result = db.query(sql, params=[recipe_id])
    return result if result else None

def get_tags():
    sql = "SELECT tag_name FROM tags"
    return db.query(sql)

def add_image(image, recipe_id):
    if not get_image(recipe_id):
        sql = "INSERT INTO recipe_images (recipe_id, recipe_image) VALUES (?, ?)"
        db.execute(sql, params=[recipe_id, image])
    else:
        sql = "UPDATE recipe_images SET recipe_image = ? WHERE recipe_id = ?"
        db.execute(sql, params=[image, recipe_id])

def get_image(recipe_id):
    sql = "SELECT recipe_image FROM recipe_images WHERE recipe_id = ?"
    result = db.query(sql, params=[recipe_id])
    return result[0][0] if result else None

def recipe_count():
    sql = "SELECT COUNT(*) FROM recipes"
    return db.query(sql)[0][0]