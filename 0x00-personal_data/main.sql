-- setup mysql server
-- configure permissions
CREATE DATABASE IF NOT EXISTS my_db;
GRANT ALL PRIVILEGES ON my_db.* TO 'pcnerd9'@'localhost';

USE my_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    email VARCHAR(256)
);

INSERT INTO users(email) VALUES ("bob@dylan.com");
INSERT INTO users(email) VALUES ("bib@dylan.com");
