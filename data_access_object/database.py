# database.py

# 標準庫導入
import os
import sys
import pickle
from contextlib import contextmanager
from typing import Optional

# 第三方庫導入
import mysql.connector

class DatabaseError(Exception):
    """資料庫操作錯誤"""
    pass

class Database:
    """主要連接我第一階段的資料庫，也就是最初儲存的使用者帳戶"""

    def __init__(self):
        self.connection: Optional[mysql.connector.MySQLConnection] = None
        self.cursor: Optional[mysql.connector.MySQLCursor] = None

    @contextmanager
    def get_cursor(self):
        """上下文管理器，提供資料庫游標"""
        try:
            yield self.cursor
        finally:
            if self.cursor:
                self.cursor.close()

    def initialize(self):
        """初始化資料庫連接並設置資料庫"""
        if self.connection and self.cursor:
            return

        config_path = self._get_config_path()
        if not os.path.exists(config_path):
            raise Exception(f"配置文件不存在或不完整: {config_path}")

        try:
            with open(config_path, 'rb') as f:
                config = pickle.load(f)

            db_config = {
                'host': config.get('host', 'localhost'),
                'user': config.get('user', ''),
                'password': config.get('password', '')
            }

            if not all(db_config.values()):
                raise Exception("配置文件中缺少 'host', 'user' 或 'password'")

            self.connection = mysql.connector.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password']
            )
            self.cursor = self.connection.cursor()

            self.create_database()
            self.connection.database = 'user_auth'
            self.initialize_database()

        except (pickle.UnpicklingError, FileNotFoundError, EOFError,
                mysql.connector.Error, KeyError) as e:
            raise Exception(f"初始化資料庫發生錯誤: {e}")

    def _get_config_path(self) -> str:
        """獲取配置文件的路徑"""
        if getattr(sys, 'frozen', False):
            return os.path.join(os.path.dirname(sys.executable), 'config.pickle')
        return os.path.join(os.path.dirname(__file__), '..', 'login', 'config.pickle')

    def create_database(self):
        """創建資料庫"""
        self._execute_query("CREATE DATABASE IF NOT EXISTS user_auth")

    def initialize_database(self):
        """初始化資料庫，檢查使用者帳戶表是否存在，如果不存在則創建"""
        self.cursor.execute("SHOW TABLES LIKE 'users'")
        if not self.cursor.fetchone():
            self.create_users_table()

    def create_users_table(self):
        """如果沒有 user 表，則創建該表"""
        create_table_query = """
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """
        self._execute_query(create_table_query)

    def check_username_exists(self, username: str) -> bool:
        """檢查帳號是否存在"""
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return self.cursor.fetchone() is not None
        except mysql.connector.Error as err:
            raise DatabaseError("查詢帳號是否存在時發生錯誤") from err

    def insert_user(self, name: str, username: str, password: str) -> bool:
        """將用戶信息插入到資料庫中"""
        try:
            self.cursor.execute(
                "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
                (name, username, password)
            )
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            raise DatabaseError("插入用戶信息時發生錯誤") from err

    def validate_user(self, username: str, password: str):
        """驗證用戶名和密碼"""
        try:
            self.cursor.execute("SELECT * FROM users WHERE username = %s"
                                , (username,))
            if self.cursor.fetchone() is None:
                return "帳號不存在"
            
            self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s"
                                , (username, password))
            if self.cursor.fetchone():
                return True
            
            return "密碼錯誤"
        
        except mysql.connector.Error as err:
            raise DatabaseError("驗證用戶名和密碼時發生錯誤") from err

    def close(self):
        """關閉資料庫連接"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except AttributeError:
            # Handle the case where cursor or connection might not be initialized
            pass

    def _execute_query(self, query: str):
        """執行資料庫查詢"""
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as err:
            raise DatabaseError("執行查詢時發生錯誤") from err

# # 標準庫導入
# import os
# import sys
# import pickle
# from contextlib import contextmanager
# from typing import Optional
# import logging

# # 第三方庫導入
# import mysql.connector
# from mysql.connector import Error as MySQLError

# class DatabaseError(Exception):
#     """資料庫操作錯誤"""
#     pass

# class Database:
#     """主要連接我第一階段的資料庫，也就是最初儲存的使用者帳戶"""

#     def __init__(self):
#         self.connection: Optional[mysql.connector.MySQLConnection] = None
#         self.cursor: Optional[mysql.connector.MySQLCursor] = None
#         self.initialize()

#     @contextmanager
#     def get_cursor(self):
#         """上下文管理器，提供資料庫游標"""
#         try:
#             self._check_connection()
#             yield self.cursor
#         finally:
#             if self.cursor:
#                 self.cursor.close()

#     def _check_connection(self):
#         """檢查資料庫連接是否有效"""
#         if self.connection is None or not self.connection.is_connected():
#             self.initialize()

#     def initialize(self):
#         """初始化資料庫連接並設置資料庫"""
#         if self.connection and self.cursor and self.connection.is_connected():
#             return

#         config_path = self._get_config_path()
#         if not os.path.exists(config_path):
#             raise Exception(f"配置文件不存在或不完整: {config_path}")

#         try:
#             with open(config_path, 'rb') as f:
#                 config = pickle.load(f)

#             db_config = {
#                 'host': config.get('host', 'localhost'),
#                 'user': config.get('user', ''),
#                 'password': config.get('password', '')
#             }

#             if not all(db_config.values()):
#                 raise Exception("配置文件中缺少 'host', 'user' 或 'password'")

#             self.connection = mysql.connector.connect(
#                 host=db_config['host'],
#                 user=db_config['user'],
#                 password=db_config['password']
#             )
#             self.cursor = self.connection.cursor()

#             self.create_database()
#             self.connection.database = 'user_auth'
#             self.initialize_database()

#         except (pickle.UnpicklingError, FileNotFoundError, EOFError,
#                 MySQLError, KeyError) as e:
#             logging.error(f"初始化資料庫發生錯誤: {e}")
#             raise Exception(f"初始化資料庫發生錯誤: {e}")

#     def _get_config_path(self) -> str:
#         """獲取配置文件的路徑"""
#         if getattr(sys, 'frozen', False):
#             return os.path.join(os.path.dirname(sys.executable), 'config.pickle')
#         return os.path.join(os.path.dirname(__file__), '..', 'login', 'config.pickle')

#     def create_database(self):
#         """創建資料庫"""
#         self._execute_query("CREATE DATABASE IF NOT EXISTS user_auth")

#     def initialize_database(self):
#         """初始化資料庫，檢查使用者帳戶表是否存在，如果不存在則創建"""
#         self.cursor.execute("SHOW TABLES LIKE 'users'")
#         if not self.cursor.fetchone():
#             self.create_users_table()

#     def create_users_table(self):
#         """如果沒有 user 表，則創建該表"""
#         create_table_query = """
#             CREATE TABLE users (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 name VARCHAR(255) NOT NULL,
#                 username VARCHAR(255) NOT NULL UNIQUE,
#                 password VARCHAR(255) NOT NULL
#             )
#         """
#         self._execute_query(create_table_query)

#     def check_username_exists(self, username: str) -> bool:
#         """檢查帳號是否存在"""
#         try:
#             self._check_connection()
#             self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
#             return self.cursor.fetchone() is not None
#         except MySQLError as err:
#             logging.error(f"查詢帳號是否存在時發生錯誤: {err}")
#             raise DatabaseError("查詢帳號是否存在時發生錯誤") from err

#     def insert_user(self, name: str, username: str, password: str) -> bool:
#         """將用戶信息插入到資料庫中"""
#         try:
#             self._check_connection()
#             self.cursor.execute(
#                 "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
#                 (name, username, password)
#             )
#             self.connection.commit()
#             return True
#         except MySQLError as err:
#             logging.error(f"插入用戶信息時發生錯誤: {err}")
#             raise DatabaseError("插入用戶信息時發生錯誤") from err

#     def validate_user(self, username: str, password: str):
#         """驗證用戶名和密碼"""
#         try:
#             self._check_connection()
#             self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
#             user = self.cursor.fetchone()
#             if user is None:
#                 return "帳號不存在"

#             self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
#             if self.cursor.fetchone():
#                 return True

#             return "密碼錯誤"
        
#         except MySQLError as err:
#             logging.error(f"驗證用戶名和密碼時發生錯誤: {err}")
#             return "資料庫錯誤"

#     def close(self):
#         """關閉資料庫連接"""
#         try:
#             if self.cursor:
#                 self.cursor.close()
#             if self.connection:
#                 self.connection.close()
#         except AttributeError:
#             # Handle the case where cursor or connection might not be initialized
#             pass

#     def _execute_query(self, query: str):
#         """執行資料庫查詢"""
#         try:
#             self._check_connection()
#             self.cursor.execute(query)
#             self.connection.commit()
#         except MySQLError as err:
#             logging.error(f"執行查詢時發生錯誤: {err}")
#             raise DatabaseError("執行查詢時發生錯誤") from err