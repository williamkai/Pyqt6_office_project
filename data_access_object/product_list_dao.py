# product_list_dao.py
import mysql.connector

class ProductListDao:

    def __init__(self,connection=None,cursor=None):
        self.connection=connection
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
        # 刪除商品
        delete_product_query = """
            DELETE FROM ProductList WHERE product_code = %s
        """

        # 刪除相關庫存記錄
        delete_inventory_query = """
            DELETE FROM Inventory WHERE product_code = %s
        """

        try:
            # 開始一個事務
            # self.connection.start_transaction()
            # 執行刪除庫存記錄操作
            self.cursor.execute(delete_inventory_query, (product_code,))

            # 執行刪除商品操作
            self.cursor.execute(delete_product_query, (product_code,))
            
            # 提交事務
            self.connection.commit()
            
            print("商品及相關庫存記錄已刪除")
            
        except mysql.connector.Error as err:
            # 回滾事務
            self.connection.rollback()
            print(f"Error deleting product or inventory records: {err}")
        
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

    