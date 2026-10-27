-- CampusEats — Assignment 7 (GraphQL): Catalogue service, dishes table
-- Run: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS campuseats_catalogue;
USE campuseats_catalogue;

DROP TABLE IF EXISTS dishes;

CREATE TABLE dishes (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(150)   NOT NULL,
    price        DECIMAL(10,2)  NOT NULL CHECK (price >= 0),
    available    TINYINT(1)     NOT NULL DEFAULT 1,
    description  VARCHAR(255)   NULL
);

INSERT INTO dishes (name, price, available, description) VALUES
    ('Veg Thali',    120.00, 1, 'Dal, sabzi, roti, rice'),
    ('Masala Dosa',   80.00, 1, 'Crispy dosa with potato filling'),
    ('Cheese Pizza', 199.00, 1, '8-inch cheese pizza'),
    ('Cold Coffee',   60.00, 0, 'Out of stock today');
