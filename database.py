import mysql.connector
import configparser

class Database:
    '''
    主要連接我第一階段的資料庫
    也就是最初儲存的使用者帳戶
    
    '''
    
    
    def __init__(self):
        self.connection = None
        self.cursor = None

    def initialize(self):
        if self.connection is not None and self.cursor is not None:
            return  # 如果已經初始化過，則不再初始化

        config = configparser.ConfigParser()
        config.read('config.ini')
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
            self.create_database()

            # 使用創建的數據庫連接
            self.connection.database = 'user_auth'

            # 執行初始化操作
            self.initialize_database()

        except mysql.connector.Error as err:
            raise Exception(f"連接資料庫失敗: {err}")

    # 創建實例時候會先執行這句話，判斷有無這個資料庫，沒有就創建
    def create_database(self):
        create_database_query = "CREATE DATABASE IF NOT EXISTS user_auth"
        self.cursor.execute(create_database_query)

    # 初始化資料庫，也就是先檢查有沒有這個表，沒有就會執行下面函數創建表
    def initialize_database(self):
        # 检查用户表是否存在，如果不存在则创建
        self.cursor.execute("SHOW TABLES LIKE 'users'")
        table_exists = self.cursor.fetchone()
        if not table_exists:
            self.create_users_table()

    # 如果沒有user就會創建這個table
    def create_users_table(self):
        create_table_query = """
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    # 這是註冊帳號時候用來確認帳號是否重複的
    def check_username_exists(self, username):
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as err:
            print("Error:", err)
            return False
        
    # 創建帳號密碼到帳號資料庫中
    def insert_user(self, name, username, password):
        try:
            self.cursor.execute("INSERT INTO users (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print("Error:", err)
            return False
        
    # 登入時候使用這個來確認有無帳號密碼
    def validate_user(self, username, password):
        try:
            # 這是確認資料庫是否有這帳號
            self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            result = self.cursor.fetchone()
            if result is None:
                return "帳號不存在"  # 帳號不存在
            else:
                # 查询数据库中是否存在匹配的用户名和密码
                self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
                result = self.cursor.fetchone()
                if result is not None:
                    return True  # 用户名和密码匹配成功
                else:
                    return "密碼錯誤"  # 密碼错误
        except mysql.connector.Error as err:
            print("Error:", err)
            return False
        
    def create_user_specific_database(self, username):
        # 創建與用戶相關的資料庫
        print("建立個別帳號資料庫~~~")
        db_name = f"user_{username}"
        create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        self.cursor.execute(create_db_query)
        self.connection.commit()

         # 切換到新創建的用戶資料庫
        self.connection.database = db_name

        # 創建 user_account_data 表格
        self.create_user_account_table()

    def create_user_account_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_account_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def insert_user_account(self, username, password):
        try:
            self.cursor.execute("INSERT INTO user_account_data (email, password) VALUES (%s, %s)", (username, password))
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print("Error:", err)
            return False

    

    def close(self):
        self.cursor.close()
        self.connection.close()