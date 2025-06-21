-- Create the database
CREATE DATABASE IF NOT EXISTS drug_responsef;

-- Use the created database
USE drug_responsef;

-- Create the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,         -- Unique identifier for each user
    username VARCHAR(255) NOT NULL UNIQUE,     -- Unique username for each user
    password VARCHAR(255) NOT NULL,            -- Password for user authentication
    is_admin BOOLEAN DEFAULT FALSE,            -- Indicates if the user is an admin
    accuracy FLOAT DEFAULT 0.0                 -- Accuracy value for the user, default set to 0.0
);
