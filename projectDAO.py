# Data Access Object class to connect to MySql Db
# Based on StudentDAO

import mysql.connector
from config import mysqlConfig

class UserDAO:
    host = ""
    user= ""
    password = ""
    database = ""

    connection =""
    cursor =""

    def __init__(self):
        self.host = mysqlConfig["host"]
        self.user = mysqlConfig["user"]
        self.password = mysqlConfig["password"]
        self.database = mysqlConfig["database"]

    def getCursor(self):
        self.connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()

        return self.cursor        

    def closeAll(self):
        self.connection.close()
        self.cursor.close()       

    # Add new user
    def create(self, name):
        cursor = self.getCursor()
        sql = "INSERT INTO user (name) VALUES (%s)"
        values = (name,)
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid      

    # Get all registered users
    def getAll(self):
        cursor = self.getCursor()
        sql = "SELECT * FROM user"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.closeAll()
        return result           

    # Get a user by the user_id
    def findByID(self, id):
        cursor = self.getCursor()
        sql = "SELECT * FROM user WHERE user_id= %s"
        values = (id,)

        cursor.execute(sql, values)

        result = cursor.fetchall()
        self.closeAll()
        return result

    def update(self, newName, id):
        cursor = self.getCursor()        
        sql = "UPDATE user SET name = %s WHERE user_id=%s"
        values = (newName, id)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()        

    def delete(self, id):
        cursor = self.getCursor()  
        sql = "DELETE FROM user WHERE user_id=%s"
        values = (id, )
        cursor.execute(sql, values)
        self.connection.commit()

        self.closeAll()

# This one's simpler, need to be able to add, remove and fetch favorites for selected user
class FavoritesDAO:
    host = ""
    user= ""
    password = ""
    database = ""

    connection =""
    cursor =""

    def __init__(self):
        self.host = mysqlConfig["host"]
        self.user = mysqlConfig["user"]
        self.password = mysqlConfig["password"]
        self.database = mysqlConfig["database"]

    def getCursor(self):
        self.connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()

        return self.cursor        

    def closeAll(self):
        self.connection.close()
        self.cursor.close()       

    # Add new user
    def create(self, user_id, album_id):
        cursor = self.getCursor()
        sql = "INSERT INTO favorites (user_id, album_id) VALUES (%s, %s)"
        values = (user_id, album_id)
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid               

    # Get user favorites by user_id
    def getFavoritesByUserID(self, user_id):
        cursor = self.getCursor()
        sql = "SELECT * FROM favorites WHERE user_id= %s"
        values = (user_id,)

        cursor.execute(sql, values)

        result = cursor.fetchall()
        self.closeAll()
        return result     
        

    def delete(self, id):
        cursor = self.getCursor()  
        sql = "DELETE FROM favorites WHERE id=%s"
        values = (id, )
        cursor.execute(sql, values)
        self.connection.commit()

        self.closeAll()


userDAO = UserDAO()
favoritesDAO = FavoritesDAO()