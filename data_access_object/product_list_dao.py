import os
import sys
import mysql.connector
import pickle
import configparser


class ProductListDao:

    def __init__(self,connectio=None,cursor=None):
        self.connectio=connectio
        self.cursor=cursor

    def create_product_list_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS ProductList (
                    product_code VARCHAR(255) PRIMARY KEY,
                    product_name VARCHAR(255) NOT NULL,
                    package_count INT NOT NULL,
                    draw_count INT NOT NULL,
                    manufacturer VARCHAR(255),
                    price DECIMAL(10, 2)
                )
            """
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error creating ProductList table: {err}")

    def get_product_list(self):
        query = "SELECT * FROM ProductList"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def delete_product(self, product_code):
        delete_query = """
            DELETE FROM ProductList WHERE product_code = %s
        """
        try:
            self.cursor.execute(delete_query, (product_code,))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error deleting from ProductList table: {err}")
    
    def insert_product(self, product_code, product_name, package_count, draw_count, manufacturer, price):
        insert_query = """
            INSERT INTO ProductList (product_code, product_name, package_count, draw_count, manufacturer, price)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_query, (product_code, product_name, package_count, draw_count, manufacturer, price))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting into ProductList table: {err}")


    def update_product(self, product_code, product_name, package_count, draw_count, manufacturer, price):
        update_query = """
            UPDATE ProductList 
            SET product_name = %s, package_count = %s, draw_count = %s, manufacturer = %s, price = %s 
            WHERE product_code = %s
        """
        try:
            self.cursor.execute(update_query, (product_name, package_count, draw_count, manufacturer, price, product_code))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error updating ProductList table: {err}")

    