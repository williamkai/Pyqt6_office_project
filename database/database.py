import os
import sys
import mysql.connector
import configparser
import pickle

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
            return
        
        # 判断是否为冻结状态，决定如何获取 config.pickle 的路径
        if getattr(sys, 'frozen', False):
            # 如果是冻结状态（打包成 exe），则使用 sys.executable 的目录
            exe_dir = os.path.dirname(sys.executable)
            config_path = os.path.join(exe_dir, 'config.pickle')
        else:
            # 如果不是冻结状态，使用当前文件所在目录的上一层目录下的 login 文件夹中的 config.pickle
            config_path = os.path.join(os.path.dirname(__file__), '..', 'login', 'config.pickle')

        # 确认配置文件路径是否存在
        if not os.path.exists(config_path):
            raise Exception(f"配置文件不存在或不完整: {config_path}")

        try:
            # 读取配置文件
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

            # 连接到数据库
            self.connection = mysql.connector.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password']
            )
            self.cursor = self.connection.cursor()

            # 如果数据库不存在则创建
            self.create_database()

            # 使用已创建的数据库连接
            self.connection.database = 'user_auth'

            # 执行其他初始化操作
            self.initialize_database()

        except (pickle.UnpicklingError, FileNotFoundError, EOFError, mysql.connector.Error, KeyError) as e:
            raise Exception(f"初始化数据库时发生错误: {e}")

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
        
    def close(self):
        self.cursor.close()
        self.connection.close()