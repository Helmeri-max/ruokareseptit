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
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TEXT
);

CREATE TABLE comments (
    comment_id INTEGER PRIMARY KEY,
    comment_content TEXT,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    sent_at TEXT,
    recipe_id INTEGER REFERENCES recipes(recipe_id) ON DELETE CASCADE
);

CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY,
    tag_name TEXT
);

CREATE TABLE recipe_tags (
    recipe_id INTEGER REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(tag_id)
);

CREATE TABLE recipe_images (
    recipe_id INTEGER REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    recipe_image BLOB 
);

INSERT INTO tags (tag_id, tag_name) VALUES
(1, 'Vegaaninen'),
(2, 'Kasvis'),
(3, 'Liha'),
(4, 'Aamiainen'),
(5, 'Lounas'),
(6, 'Päivällinen'),
(7, 'Välipala'),
(8, 'Laktoositon'),
(9, 'Gluteeniton');

CREATE INDEX idx_recipe ON recipes (recipe_id, user_id);
CREATE INDEX idx_comments ON comments (recipe_id);
CREATE INDEX idx_comments_composite ON comments (recipe_id, sent_at DESC);
CREATE INDEX idx_tags ON recipe_tags (recipe_id);
CREATE INDEX idx_images ON recipe_images (recipe_id);