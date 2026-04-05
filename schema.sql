-- Run this to set up the database
-- mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS sales_dashboard;
USE sales_dashboard;

CREATE TABLE IF NOT EXISTS sales (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    date     DATE NOT NULL,
    product  VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price    DECIMAL(10,2) NOT NULL,
    revenue  DECIMAL(10,2) NOT NULL,
    region   VARCHAR(100) NOT NULL
);
