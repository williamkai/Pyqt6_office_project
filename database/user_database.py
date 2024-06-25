import mysql.connector
import configparser

class UserDatabase:
    '''
    主要連接我第二階段的資料庫
    也就是使用者帳戶的資料庫
    
    ''' 
    def __init__(self,user_email):
        self.connection = None
        self.cursor = None
        self.username=user_email
        self.initialize()

    def initialize(self):
        if self.connection is not None and self.cursor is not None:
            return  # 如果已經初始化過，則不再初始化

        config = configparser.ConfigParser()
        config.read('login\config.ini')
        if 'database' not in config:
            raise Exception("配置文件不存在或不完整")
        for key in ['host', 'user', 'password']:
            if key not in config['database'] or not config['database'][key]:
                return Exception("配置文件不存在或不完整")

        db_config = {
            'host': config.get('database', 'host'),
            'user': config.get('database', 'user'),
            'password': config.get('database', 'password')
        }

        try:
            # 連接到資料庫
            self.connection = mysql.connector.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password']
            )
            self.cursor = self.connection.cursor()

            # 沒有資料庫的話就創建一個
            db_name = f"user_{self.username}"
            self.create_database(db_name)

            # 使用創建的數據庫連接
            self.connection.database = f'{db_name}'

            # 執行初始化操作
            self.initialize_database()

        except mysql.connector.Error as err:
            raise Exception(f"連接資料庫失敗: {err}")

    # 創建實例時候會先執行這句話，判斷有無這個資料庫，沒有就創建
    def create_database(self,db_name):
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        self.cursor.execute(create_database_query)

    # 初始化資料庫，也就是先檢查有沒有這個表，沒有就會執行下面函數創建表
    def initialize_database(self):
        # 检查用户表是否存在，如果不存在则创建
        self.cursor.execute("SHOW TABLES LIKE 'User_basic_information'")
        table_exists = self.cursor.fetchone()
        if not table_exists:
            self.create_User_basic_information_table()

    # 如果沒有user就會創建這個table
    def create_User_basic_information_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS User_basic_information (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error creating table: {err}")
               
    def insert_user_account(self, username, password):
        try:
            self.cursor.execute("INSERT INTO User_basic_information (email, password) VALUES (%s, %s)", (username, password))
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print("Error:", err)
            return False
        
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


    def create_inventory_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS Inventory (
                inventory_id INT AUTO_INCREMENT PRIMARY KEY,
                product_code VARCHAR(255) NOT NULL,
                date DATETIME NOT NULL,
                status ENUM('製造', '銷貨', '退貨', '瑕疵品') NOT NULL,
                quantity INT NOT NULL,
                FOREIGN KEY (product_code) REFERENCES ProductList(product_code)
            )
        """
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Inventory table created successfully.")
        except mysql.connector.Error as err:
            print(f"Error creating Inventory table: {err}")


    def search_inventory(self, product_code):
        search_query = """
            SELECT inventory_id, product_code, date, status, quantity
            FROM Inventory
            WHERE product_code = %s
        """
        try:
            self.cursor.execute(search_query, (product_code,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error searching inventory: {err}")
            return []
        
    def get_all_product_codes(self):
        query = "SELECT product_code FROM ProductList"
        self.cursor.execute(query)
        return [item[0] for item in self.cursor.fetchall()]

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
        except mysql.connector.Error as err:
            print(f"Error closing the database connection: {err}")
