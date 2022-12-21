# Data Access Object class to connect to MySql Db
# Based on StudentDAO

import mysql.connector
from config import mysqlConfig


def createDB():
    db = mysqlConfig["database"]

    connection = mysql.connector.connect(
            host = mysqlConfig["host"],
            user = mysqlConfig["user"],
            password = mysqlConfig["password"],
            auth_plugin='mysql_native_password'
        )

    cursor = connection.cursor()

    # remove database if it was sreated before
    cursor.execute("DROP DATABASE IF EXISTS project")

    cursor.execute("CREATE DATABASE project")

    connection.close()
    cursor.close()


def createTables():

    connection = mysql.connector.connect(
            host = mysqlConfig["host"],
            user = mysqlConfig["user"],
            password = mysqlConfig["password"],
            database = mysqlConfig["database"],
            auth_plugin='mysql_native_password'
        )

    cursor = connection.cursor()    

    # Create user table
    cursor.execute("CREATE TABLE user (user_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, name VARCHAR(250) NOT NULL)")
    # Creat favorites table, with user_id being foreign key to user table
    cursor.execute("CREATE TABLE favorites (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, user_id INT NOT NULL, album_id INT NOT NULL, FOREIGN KEY (user_id) REFERENCES user(user_id))") 

    connection.close()
    cursor.close()



if(__name__=="__main__"):

    createDB()
    createTables()

    