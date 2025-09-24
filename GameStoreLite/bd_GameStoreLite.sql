-- Crear base de datos y usarla
CREATE DATABASE IF NOT EXISTS GameStoreLite;
USE GameStoreLite;

-- Borrar tablas en orden correcto (por dependencias)
DROP TABLE IF EXISTS SaleDetails;
DROP TABLE IF EXISTS Sales;
DROP TABLE IF EXISTS Games;
DROP TABLE IF EXISTS Genres;
DROP TABLE IF EXISTS Customers;

-- Borrar procedimientos si existen
DROP PROCEDURE IF EXISTS sp_InsertGenre;
DROP PROCEDURE IF EXISTS sp_InsertCustomer;
DROP PROCEDURE IF EXISTS sp_InsertGame;
DROP PROCEDURE IF EXISTS sp_InsertSale;
DROP PROCEDURE IF EXISTS sp_InsertSaleDetail;

START TRANSACTION;

-- 1. Tabla de géneros
CREATE TABLE Genres (
    GenreID INT PRIMARY KEY AUTO_INCREMENT,
    GenreName VARCHAR(30) NOT NULL,
    Description VARCHAR(255)
);

-- 2. Tabla de clientes
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    FullName VARCHAR(60) NOT NULL,
    Email VARCHAR(50),
    City VARCHAR(25),
    Country VARCHAR(20)
);

-- 3. Tabla de videojuegos
CREATE TABLE Games (
    GameID INT PRIMARY KEY AUTO_INCREMENT,
    GameTitle VARCHAR(60) NOT NULL,
    GenreID INT,
    Platform VARCHAR(25),
    Price DECIMAL(8,2),
    FOREIGN KEY (GenreID) REFERENCES Genres(GenreID)
);

-- 4. Tabla de ventas
CREATE TABLE Sales (
    SaleID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    SaleDate DATETIME,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- 5. Detalles de cada venta
CREATE TABLE SaleDetails (
    SaleDetailID INT PRIMARY KEY AUTO_INCREMENT,
    SaleID INT,
    GameID INT,
    Quantity INT,
    FOREIGN KEY (SaleID) REFERENCES Sales(SaleID),
    FOREIGN KEY (GameID) REFERENCES Games(GameID)
);

COMMIT;

-- Crear procedimientos almacenados
DELIMITER $$

-- Insertar género
CREATE PROCEDURE sp_InsertGenre(
    IN p_GenreName VARCHAR(100),
    IN p_Description TEXT
)
BEGIN
    INSERT INTO Genres (GenreName, Description)
    VALUES (p_GenreName, p_Description);
END$$

-- Insertar cliente
CREATE PROCEDURE sp_InsertCustomer(
    IN p_FullName VARCHAR(60),
    IN p_Email VARCHAR(50),
    IN p_City VARCHAR(25),
    IN p_Country VARCHAR(20)
)
BEGIN
    INSERT INTO Customers (FullName, Email, City, Country)
    VALUES (p_FullName, p_Email, p_City, p_Country);
END$$

-- Insertar juego
CREATE PROCEDURE sp_InsertGame(
    IN p_GameTitle VARCHAR(60),
    IN p_GenreID INT,
    IN p_Platform VARCHAR(25),
    IN p_Price DECIMAL(8,2)
)
BEGIN
    INSERT INTO Games (GameTitle, GenreID, Platform, Price)
    VALUES (p_GameTitle, p_GenreID, p_Platform, p_Price);
END$$

-- Insertar venta
CREATE PROCEDURE sp_InsertSale(
    IN p_CustomerID INT,
    IN p_SaleDate DATETIME
)
BEGIN
    INSERT INTO Sales (CustomerID, SaleDate)
    VALUES (p_CustomerID, p_SaleDate);
END$$

-- Insertar detalle de venta
CREATE PROCEDURE sp_InsertSaleDetail(
    IN p_SaleID INT,
    IN p_GameID INT,
    IN p_Quantity INT
)
BEGIN
    INSERT INTO SaleDetails (SaleID, GameID, Quantity)
    VALUES (p_SaleID, p_GameID, p_Quantity);
END$$

DELIMITER ;

-- Comprobar tablas y procedimientos
SHOW TABLES;
SHOW PROCEDURE STATUS WHERE Db = 'GameStoreLite';


