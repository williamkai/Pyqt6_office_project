import os
import sys
import mysql.connector
import pickle
import configparser

from data_access_object.product_list_dao import ProductListDao
from data_access_object.inventory_dao import InventoryDao
from data_access_object.customer_dao import CustomerInformationDao
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
        self.product_list_dao=ProductListDao(self.connection,self.cursor)
        self.inventory_dao=InventoryDao(self.connection,self.cursor)
        self.customer_dao=CustomerInformationDao(self.connection,self.cursor)

    def initialize(self):
        if self.connection is not None and self.cursor is not None:
            return
        
        # 判断是否為封裝状态，决定如何取得 config.pickle 的路径
        if getattr(sys, 'frozen', False):
            # 如果是封裝狀態（也就是打包成 exe），則使用 sys.executable 的目錄(也就是此exe檔案的目錄)
            exe_dir = os.path.dirname(sys.executable)
            config_path = os.path.join(exe_dir, 'config.pickle')
        else:
            # 如果不是封裝狀態，使用目前文件所在目錄的上一層目錄下的 login 文件夾中的 config.pickle
            config_path = os.path.join(os.path.dirname(__file__), '..', 'login', 'config.pickle')

        # 確認配置文件路徑是否存在
        if not os.path.exists(config_path):
            raise Exception(f"配置文件不存在或不完整: {config_path}")

        try:
            # 讀取配置文件
            with open(config_path, 'rb') as f:
                config = pickle.load(f)

            # 確認配置的完整性
            db_config = {
                'host': config.get('host', 'localhost'),
                'user': config.get('user', ''),
                'password': config.get('password', '')
            }

            if not all(db_config.values()):
                raise Exception("配置文件中缺少 'host', 'user' 或 'password'")

            # 連接到資料庫
            self.connection = mysql.connector.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password']
            )
            self.cursor = self.connection.cursor()  # 這是我除bug用到的東西，太久沒用忘記這啥了，dictionary=True

            # 創建個別帳戶使用的資料庫
            db_name = f"user_{self.username}"
            self.create_database(db_name)

            # 使用新創建的資料庫或者說個別帳號的資料庫
            self.connection.database = f'{db_name}'

            # 初始化資料庫結構
            self.initialize_database()

        except mysql.connector.Error as err:
            raise Exception(f"無法連接資料庫: {err}")

    # 創建實例時候會先執行這句話，判斷有無這個資料庫，沒有就創建
    def create_database(self,db_name):
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        self.cursor.execute(create_database_query)

    # 初始化資料庫，也就是先檢查有沒有這個表，沒有就會執行下面函數創建表
    def initialize_database(self):
        # 檢查帳戶表是否存在，如果不存在則創建，這是基礎用戶個別資料表，目前只是要用來連信箱，所以沒啥特別東西，這個表就只有信箱資料
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
            # 檢查表格是否已經有資料
            self.cursor.execute("SELECT COUNT(*) FROM User_basic_information")
            count = self.cursor.fetchone()[0]
            
            if count > 0:
                # 表格已有資料，執行更新操作
                self.cursor.execute(
                    "UPDATE User_basic_information SET email = %s, password = %s WHERE id = 1",
                    (username, password)
                )
            else:
                # 表格沒有資料，執行插入操作
                self.cursor.execute(
                    "INSERT INTO User_basic_information (email, password) VALUES (%s, %s)",
                    (username, password)
                )
            
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print("Error:", err)
            return False
    def fetch_user_data(self):
        """ 從資料庫中獲取用戶數據 """
        query = "SELECT email, password FROM User_basic_information WHERE id = 1"  # 根據實際情況修改查詢語句
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        
        if result:
            email, password = result
            return {
                "信箱功能帳號": email,
                "密碼": password,
                "再次確認密碼": password
            }
        else:
            # 若沒有資料則返回空字典
            return {
                "信箱功能帳號": "",
                "密碼": "",
                "再次確認密碼": ""
            }

        # try:
        #     self.cursor.execute("INSERT INTO User_basic_information (email, password) VALUES (%s, %s)", (username, password))
        #     self.connection.commit()
        #     return True
        # except mysql.connector.Error as err:
        #     print("Error:", err)
        #     return False

 ########這邊下面是產品清單的資料庫dao       
    # def create_product_list_table(self):
    #     create_table_query = """
    #         CREATE TABLE IF NOT EXISTS ProductList (
    #                 product_code VARCHAR(255) PRIMARY KEY,
    #                 product_name VARCHAR(255) NOT NULL,
    #                 package_count INT NOT NULL,
    #                 draw_count INT NOT NULL,
    #                 manufacturer VARCHAR(255),
    #                 price DECIMAL(10, 2)
    #             )
    #         """
    #     try:
    #         self.cursor.execute(create_table_query)
    #         self.connection.commit()
    #     except mysql.connector.Error as err:
    #         print(f"Error creating ProductList table: {err}")

    # def get_product_list(self):
    #     query = "SELECT * FROM ProductList"
    #     self.cursor.execute(query)
    #     return self.cursor.fetchall()
    
    # def delete_product(self, product_code):
    #     delete_query = """
    #         DELETE FROM ProductList WHERE product_code = %s
    #     """
    #     try:
    #         self.cursor.execute(delete_query, (product_code,))
    #         self.connection.commit()
    #     except mysql.connector.Error as err:
    #         print(f"Error deleting from ProductList table: {err}")
    
    # def insert_product(self, product_code, product_name, package_count, draw_count, manufacturer, price):
    #     insert_query = """
    #         INSERT INTO ProductList (product_code, product_name, package_count, draw_count, manufacturer, price)
    #         VALUES (%s, %s, %s, %s, %s, %s)
    #     """
    #     try:
    #         self.cursor.execute(insert_query, (product_code, product_name, package_count, draw_count, manufacturer, price))
    #         self.connection.commit()
    #     except mysql.connector.Error as err:
    #         print(f"Error inserting into ProductList table: {err}")


    # def update_product(self, product_code, product_name, package_count, draw_count, manufacturer, price):
    #     update_query = """
    #         UPDATE ProductList 
    #         SET product_name = %s, package_count = %s, draw_count = %s, manufacturer = %s, price = %s 
    #         WHERE product_code = %s
    #     """
    #     try:
    #         self.cursor.execute(update_query, (product_name, package_count, draw_count, manufacturer, price, product_code))
    #         self.connection.commit()
    #     except mysql.connector.Error as err:
    #         print(f"Error updating ProductList table: {err}")

####################到這邊
    # def create_inventory_table(self):
    #     create_table_query = """
    #         CREATE TABLE IF NOT EXISTS Inventory (
    #             inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    #             product_code VARCHAR(255) NOT NULL,
    #             date DATETIME NOT NULL,
    #             status ENUM('製造', '銷貨', '退貨', '瑕疵品') NOT NULL,
    #             quantity INT NOT NULL,
    #             current_stock INT,
    #             notes TEXT DEFAULT NULL,
    #             FOREIGN KEY (product_code) REFERENCES ProductList(product_code)
    #         )
    #     """
    #     try:
    #         self.cursor.execute(create_table_query)
    #         self.connection.commit()
    #         print("Inventory table created successfully.")
    #     except mysql.connector.Error as err:
    #         print(f"Error creating Inventory table: {err}")
        
    #     # 如果表已经存在，添加 current_stock 列
    #     try:
    #         self.cursor.execute("ALTER TABLE Inventory ADD COLUMN current_stock INT")
    #         self.connection.commit()
    #         print("Added current_stock column to Inventory table.")
    #     except mysql.connector.Error as err:
    #         if "Duplicate column name 'current_stock'" in str(err):
    #             print("current_stock column already exists.")#這來判斷有沒有這欄位，但通常都有，因為我前面創建已經加進去了
    #         else:
    #             print(f"Error adding current_stock column to Inventory table: {err}")


    # def search_inventory(self, product_code):
    #     search_query = """
    #         SELECT inventory_id, product_code, date, status, quantity, current_stock, notes
    #         FROM Inventory
    #         WHERE product_code = %s
    #         ORDER BY date DESC
    #     """
    #     try:
    #         self.cursor.execute(search_query, (product_code,))
    #         return self.cursor.fetchall()
    #     except mysql.connector.Error as err:
    #         print(f"Error searching inventory: {err}")
    #         return []
        
    # def update_inventory(self, inventory_id, product_code, date, status, quantity):
    #     try:
    #         # 获取当前库存量
    #         get_current_stock_query = """
    #             SELECT current_stock FROM Inventory
    #             WHERE inventory_id = %s
    #         """
    #         self.cursor.execute(get_current_stock_query, (inventory_id,))
    #         result = self.cursor.fetchone()
    #         current_stock = result[0] if result else 0

    #         # 根据操作状态更新库存量
    #         if status == '製造':
    #             current_stock += quantity
    #         elif status in ['銷貨', '瑕疵品']:
    #             current_stock -= quantity
    #         elif status == '退貨':
    #             current_stock += quantity

    #         # 更新库存记录
    #         update_query = """
    #             UPDATE Inventory
    #             SET product_code = %s, date = %s, status = %s, quantity = %s, current_stock = %s
    #             WHERE inventory_id = %s
    #         """
    #         self.cursor.execute(update_query, (product_code, date, status, quantity, current_stock, inventory_id))
    #         self.connection.commit()
    #     except mysql.connector.Error as err:
    #         print(f"Error updating Inventory table: {err}")

    # def delete_inventory(self, inventory_id, product_code):
    #  # 查找要刪除的庫存記錄
    #     get_inventory_query = """
    #         SELECT date, status, quantity, current_stock
    #         FROM Inventory
    #         WHERE inventory_id = %s
    #     """
    #     self.cursor.execute(get_inventory_query, (inventory_id,))
    #     inventory_record = self.cursor.fetchone()

    #     if inventory_record:
    #         date = inventory_record[0]
    #         status = inventory_record[1]
    #         quantity = inventory_record[2]
    #         current_stock = inventory_record[3]

    #         # 計算庫存變動量
    #         if status == '製造':
    #             update_quantity = -quantity
    #         elif status == '銷貨' or status == '瑕疵品':
    #             update_quantity = quantity  # 銷貨和瑕疵品是減少庫存，所以刪除時應該增加庫存
    #         elif status == '退貨':
    #             update_quantity = -quantity  # 退貨是增加庫存，所以刪除時應該減少庫存

    #         # 刪除庫存記錄
    #         delete_query = """
    #             DELETE FROM Inventory WHERE inventory_id = %s
    #         """
    #         try:
    #             self.cursor.execute(delete_query, (inventory_id,))
    #             self.connection.commit()

    #             # 調整從刪除日期後的所有庫存記錄的 current_stock
    #             adjust_query = """
    #                 UPDATE Inventory
    #                 SET current_stock = current_stock + %s
    #                 WHERE product_code = %s AND date > %s
    #             """
    #             self.cursor.execute(adjust_query, (update_quantity, product_code, date))
    #             self.connection.commit()

    #         except mysql.connector.Error as err:
    #             print(f"Error deleting from Inventory table: {err}")
    #     else:
    #         print(f"No inventory record found with inventory_id: {inventory_id}")

    #    #####這個雖然有 roduct_codes，但是是用來處理庫存資料庫的搜索功能
    # def get_all_product_codes(self):
    #     query = "SELECT product_code FROM ProductList"
    #     self.cursor.execute(query)
    #     return [item[0] for item in self.cursor.fetchall()]
    

    # def insert_inventory(self, product_code, date, status, quantity, notes):
    #     try:
    #         # 查询最近一次庫存記錄的 current_stock
    #         get_current_stock_query = """
    #             SELECT current_stock FROM Inventory
    #             WHERE product_code = %s
    #             ORDER BY date DESC
    #             LIMIT 1
    #         """
    #         self.cursor.execute(get_current_stock_query, (product_code,))
    #         result = self.cursor.fetchone()
            
    #         if result:
    #             current_stock = result[0]
    #         else:
    #             current_stock = 0
            
    #         # 根据操作类型更新 current_stock
    #         if status == '製造':
    #             current_stock += quantity
    #         elif status in ['銷貨', '瑕疵品']:
    #             current_stock -= quantity
    #         elif status == '退貨':
    #             current_stock += quantity

    #         # 插入新的庫存記錄
    #         insert_query = """
    #             INSERT INTO Inventory (product_code, date, status, quantity, current_stock, notes)
    #             VALUES (%s, %s, %s, %s, %s, %s)
    #         """
    #         self.cursor.execute(insert_query, (product_code, date, status, quantity, current_stock, notes))
    #         self.connection.commit()
    #         print("庫存記錄插入成功")
            
    #     except mysql.connector.Error as err:
    #         print(f"插入庫存記錄時出錯: {err}")

    #     # 在你的資料庫類別中新增這個方法
    # def adjust_inventory_after_date(self, inventory_id, product_code, date, status, quantity, current_stock, notes):
    #     try:
    #         # 獲取前一筆庫存記錄的 current_stock
    #         get_previous_inventory_query = """
    #             SELECT inventory_id, current_stock, quantity
    #             FROM Inventory
    #             WHERE product_code = %s AND date < %s
    #             ORDER BY date DESC
    #             LIMIT 1
    #         """
    #         self.cursor.execute(get_previous_inventory_query, (product_code, date))
    #         previous_result = self.cursor.fetchone()

    #         if previous_result:
    #             previous_inventory_id = previous_result[0]
    #             previous_current_stock = previous_result[1]
    #             previous_quantity = previous_result[2]
    #         else:
    #             previous_inventory_id = None
    #             previous_current_stock = 0
    #             previous_quantity = 0

    #         # 計算庫存變動量
    #         if status == '製造':
    #             update_current_stock = previous_current_stock + quantity
    #         elif status == '銷貨' or status == '瑕疵品':
    #             update_current_stock = previous_current_stock - quantity  # 銷貨和瑕疵品是減少庫存
    #         elif status == '退貨':
    #             update_current_stock = previous_current_stock + quantity  # 退貨是增加庫存

    #         # 更新當前庫存記錄
    #         update_query = """
    #             UPDATE Inventory
    #             SET product_code = %s, date = %s, status = %s, quantity = %s, current_stock = %s, notes = %s
    #             WHERE inventory_id = %s
    #         """
    #         self.cursor.execute(update_query, (product_code, date, status, quantity, update_current_stock, notes, inventory_id))
    #         self.connection.commit()

    #         # 調整從變動日期後的所有庫存記錄的 current_stock
    #         update_quantity = update_current_stock - current_stock
    #         print(f"{update_quantity}")
    #         print(f"{update_current_stock}")
    #         print(f"{current_stock}")
    #         if update_quantity > 0:
    #             print("到底是不是執行這邊? 這邊明明是+，我明明是負數為啥執行這邊")
    #             adjust_query = """
    #                 UPDATE Inventory
    #                 SET current_stock = current_stock + %s
    #                 WHERE product_code = %s AND date > %s
    #             """
    #         else:
    #             print("應該是要執行這邊才對啊")
    #             adjust_query = """
    #                 UPDATE Inventory
    #                 SET current_stock = current_stock + %s
    #                 WHERE product_code = %s AND date > %s
    #             """

    #         self.cursor.execute(adjust_query, (update_quantity, product_code, date))
    #         self.connection.commit()

    #     except mysql.connector.Error as err:
    #         print(f"Error adjusting inventory after date: {err}")


    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
        except mysql.connector.Error as err:
            print(f"Error closing the database connection: {err}")
