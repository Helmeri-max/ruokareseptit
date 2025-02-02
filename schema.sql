CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    recipe_id INTEGER PRIMARY KEY,
    title TEXT,
    ingredients TEXT,
    instructions TEXT,
    user_id INTEGER REFERENCES users,
    created_at TEXT
);

CREATE TABLE comments (
    comment_id INTEGER PRIMARY KEY,
    comment_content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TEXT,
    recipe_id INTEGER REFERENCES recipes
);
