CREATE DATABASE IF NOT EXISTS capstone_db;

CREATE TABLE capstone_db.posts (
    id INT AUTO_INCREMENT,
    post_id INT NOT NULL,
    board_id INT NOT NULL,
    content TEXT NOT NULL,
    user_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    PRIMARY KEY (id),
    UNIQUE KEY unique_post_board (post_id, board_id)
);

DROP TABLE IF EXISTS my_test_db.posts;

CREATE TABLE capstone_db.users (
    user_id INT AUTO_INCREMENT,
    user_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE capstone_db.categories (
    id INT AUTO_INCREMENT,
    post_id INT,
    board_id INT,
    pred_category VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id, board_id) REFERENCES posts(post_id, board_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    PRIMARY KEY (id),
    UNIQUE KEY unique_post_board (post_id, board_id)
);

DROP TABLE IF EXISTS capstone_db.scores;

CREATE TABLE capstone_db.scores (
    id INT AUTO_INCREMENT,
    post_id INT,
    board_id INT,
    pred_abuse_score FLOAT,
    pred_abuse_flag INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id, board_id) REFERENCES posts(post_id, board_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    PRIMARY KEY (id),
    UNIQUE KEY unique_post_board (post_id, board_id)
);

CREATE TABLE smki_capstone_db.scores (
    id INT AUTO_INCREMENT,
    post_id INT,
    board_id INT,
    pred_abuse_score FLOAT,
    pred_abuse_flag INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id, board_id) REFERENCES posts(post_id, board_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    PRIMARY KEY (id),
    UNIQUE KEY unique_post_board (post_id, board_id)
);

CREATE TABLE capstone_db.docs (
    id INT AUTO_INCREMENT,
    post_id INT,
    board_id INT,
    pred_id VARCHAR(100),
    pred_post_id INT,
    pred_board_id INT,
    cosine_distance FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id, board_id) REFERENCES posts(post_id, board_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    PRIMARY KEY (id)
);


INSERT INTO capstone_db.users (user_name) VALUES ('Baek');