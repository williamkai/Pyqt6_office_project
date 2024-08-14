#User_basic_information_dao.py
import mysql.connector

class UserBasicInformationDAO:

    def __init__(self,connection=None,cursor=None):
        self.connection=connection
        self.cursor=cursor



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