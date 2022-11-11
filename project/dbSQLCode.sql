CREATE DATABASE IF NOT EXISTS dianProject;

USE dianProject;

CREATE TABLE user(
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(1000) DEFAULT NULL,
    email varchar(100) DEFAULT NULL,
    password VARCHAR(100) NOT NULL,
    rol varchar(100) DEFAULT NULL,
    PRIMARY KEY(id)
)CHARACTER SET utf8 COLLATE utf8_general_ci;


INSERT INTO user(name, email, password, rol) values("Juan Sebastian ", "juanc7795@gmail.com","1234","admin");