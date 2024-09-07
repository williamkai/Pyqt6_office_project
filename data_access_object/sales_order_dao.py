# sales_order_dao.py
import mysql.connector

class SalesOrderDao:

    def __init__(self, connection=None, cursor=None):
        self.connection = connection
        self.cursor = cursor

    def create_sales_order_table(self):
        create_sales_order_table_query = """
            CREATE TABLE IF NOT EXISTS SalesOrder (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id VARCHAR(255) UNIQUE NOT NULL,
                company_name VARCHAR(255) NOT NULL,
                order_date DATETIME NOT NULL,
                total_amount DECIMAL(10, 2) DEFAULT NULL,
                status ENUM('已完成', '待出貨', '已取消') NOT NULL,
                settled ENUM('已結帳', '未結帳') NOT NULL,
                FOREIGN KEY (company_name) REFERENCES Customers(CompanyName)
            )
        """
        try:
            self.cursor.execute(create_sales_order_table_query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error creating CustomerInformation table: {err}")

    def create_sales_order_detail_table(self):
        create_sales_order_detail_query = """
            CREATE TABLE IF NOT EXISTS SalesOrderDetail (
                detail_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id VARCHAR(255) NOT NULL,
                product_code VARCHAR(255) NOT NULL,
                quantity INT NOT NULL,
                unit_price DECIMAL(10, 2) NOT NULL,
                notes TEXT DEFAULT NULL,
                FOREIGN KEY (order_id) REFERENCES SalesOrder(order_id),
                FOREIGN KEY (product_code) REFERENCES ProductList(product_code)
            )
        """
        try:
            self.cursor.execute(create_sales_order_detail_query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error creating CustomerInformation table: {err}")
