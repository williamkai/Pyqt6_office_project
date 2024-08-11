# inventory_dao.py

import mysql.connector


class InventoryDao:

    def __init__(self,connection=None,cursor=None):
        self.connection=connection
        self.cursor=cursor


    def create_inventory_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS Inventory (
                inventory_id INT AUTO_INCREMENT PRIMARY KEY,
                product_code VARCHAR(255) NOT NULL,
                date DATETIME NOT NULL,
                status ENUM('製造', '銷貨', '退貨', '瑕疵品') NOT NULL,
                quantity INT NOT NULL,
                current_stock INT,
                notes TEXT DEFAULT NULL,
                FOREIGN KEY (product_code) REFERENCES ProductList(product_code)
            )
        """
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Inventory table created successfully.")
        except mysql.connector.Error as err:
            print(f"Error creating Inventory table: {err}")
        
        # 如果表已经存在，添加 current_stock 列
        try:
            self.cursor.execute("ALTER TABLE Inventory ADD COLUMN current_stock INT")
            self.connection.commit()
            print("Added current_stock column to Inventory table.")
        except mysql.connector.Error as err:
            if "Duplicate column name 'current_stock'" in str(err):
                print("current_stock column already exists.")#這來判斷有沒有這欄位，但通常都有，因為我前面創建已經加進去了
            else:
                print(f"Error adding current_stock column to Inventory table: {err}")


    def search_inventory(self, product_code):
        search_query = """
            SELECT inventory_id, product_code, date, status, quantity, current_stock, notes
            FROM Inventory
            WHERE product_code = %s
            ORDER BY UNIX_TIMESTAMP(date) DESC
        """
        try:
            self.cursor.execute(search_query, (product_code,))
            result = self.cursor.fetchall()
            print(result)  # 列印查詢結果，確認順序
            return result
        except mysql.connector.Error as err:
            print(f"Error searching inventory: {err}")
            return []
        
    def get_latest_inventory(self, product_code):
        search_query = """
            SELECT current_stock
            FROM Inventory
            WHERE product_code = %s
            ORDER BY UNIX_TIMESTAMP(date) DESC
            LIMIT 1
        """
        try:
            self.cursor.execute(search_query, (product_code,))
            result = self.cursor.fetchone()  # 只取得一條記錄
            return result[0] if result else None  # 返回庫存量，或者如果沒有記錄返回None
        except mysql.connector.Error as err:
            print(f"Error fetching latest inventory: {err}")
            return None

    def update_inventory(self, inventory_id, product_code, date, status, quantity):
        try:
            # 获取当前库存量
            get_current_stock_query = """
                SELECT current_stock FROM Inventory
                WHERE inventory_id = %s
            """
            self.cursor.execute(get_current_stock_query, (inventory_id,))
            result = self.cursor.fetchone()
            current_stock = result[0] if result else 0

            # 根据操作状态更新库存量
            if status == '製造':
                current_stock += quantity
            elif status in ['銷貨', '瑕疵品']:
                current_stock -= quantity
            elif status == '退貨':
                current_stock += quantity

            # 更新库存记录
            update_query = """
                UPDATE Inventory
                SET product_code = %s, date = %s, status = %s, quantity = %s, current_stock = %s
                WHERE inventory_id = %s
            """
            self.cursor.execute(update_query, (product_code, date, status, quantity, current_stock, inventory_id))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error updating Inventory table: {err}")

    def delete_inventory(self, inventory_id, product_code):
     # 查找要刪除的庫存記錄
        get_inventory_query = """
            SELECT date, status, quantity, current_stock
            FROM Inventory
            WHERE inventory_id = %s
        """
        self.cursor.execute(get_inventory_query, (inventory_id,))
        inventory_record = self.cursor.fetchone()

        if inventory_record:
            date = inventory_record[0]
            status = inventory_record[1]
            quantity = inventory_record[2]
            current_stock = inventory_record[3]

            # 計算庫存變動量
            if status == '製造':
                update_quantity = -quantity
            elif status == '銷貨' or status == '瑕疵品':
                update_quantity = quantity  # 銷貨和瑕疵品是減少庫存，所以刪除時應該增加庫存
            elif status == '退貨':
                update_quantity = -quantity  # 退貨是增加庫存，所以刪除時應該減少庫存

            # 刪除庫存記錄
            delete_query = """
                DELETE FROM Inventory WHERE inventory_id = %s
            """
            try:
                self.cursor.execute(delete_query, (inventory_id,))
                self.connection.commit()

                # 調整從刪除日期後的所有庫存記錄的 current_stock
                adjust_query = """
                    UPDATE Inventory
                    SET current_stock = current_stock + %s
                    WHERE product_code = %s AND date > %s
                """
                self.cursor.execute(adjust_query, (update_quantity, product_code, date))
                self.connection.commit()

            except mysql.connector.Error as err:
                print(f"Error deleting from Inventory table: {err}")
        else:
            print(f"No inventory record found with inventory_id: {inventory_id}")

       #####這個雖然有 roduct_codes，但是是用來處理庫存資料庫的搜索功能
    def get_all_product_codes(self):
        query = "SELECT product_code FROM ProductList"
        self.cursor.execute(query)
        return [item[0] for item in self.cursor.fetchall()]
    

    def insert_inventory(self, product_code, date, status, quantity, notes):
        try:
            # 查询最近一次庫存記錄的 current_stock
            get_current_stock_query = """
                SELECT current_stock FROM Inventory
                WHERE product_code = %s
                ORDER BY date DESC
                LIMIT 1
            """
            self.cursor.execute(get_current_stock_query, (product_code,))
            result = self.cursor.fetchone()
            
            if result:
                current_stock = result[0]
            else:
                current_stock = 0
            
            # 根据操作类型更新 current_stock
            if status == '製造':
                current_stock += quantity
            elif status =='銷貨':
                current_stock -= quantity
            elif status == '瑕疵品':
                current_stock -= quantity
            elif status == '退貨':
                current_stock += quantity

            # 插入新的庫存記錄
            insert_query = """
                INSERT INTO Inventory (product_code, date, status, quantity, current_stock, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (product_code, date, status, quantity, current_stock, notes))
            self.connection.commit()
            print("庫存記錄插入成功")
            
        except mysql.connector.Error as err:
            print(f"插入庫存記錄時出錯: {err}")

        # 在你的資料庫類別中新增這個方法
    def adjust_inventory_after_date(self, inventory_id, product_code, date, status, quantity, current_stock, notes):
        try:
            # 獲取前一筆庫存記錄的 current_stock
            get_previous_inventory_query = """
                SELECT inventory_id, current_stock, quantity
                FROM Inventory
                WHERE product_code = %s AND date < %s
                ORDER BY date DESC
                LIMIT 1
            """
            self.cursor.execute(get_previous_inventory_query, (product_code, date))
            previous_result = self.cursor.fetchone()

            if previous_result:
                previous_inventory_id = previous_result[0]
                previous_current_stock = previous_result[1]
                previous_quantity = previous_result[2]
            else:
                previous_inventory_id = None
                previous_current_stock = 0
                previous_quantity = 0

            # 計算庫存變動量
            if status == '製造':
                update_current_stock = previous_current_stock + quantity
            elif status == '銷貨' or status == '瑕疵品':
                update_current_stock = previous_current_stock - quantity  # 銷貨和瑕疵品是減少庫存
            elif status == '退貨':
                update_current_stock = previous_current_stock + quantity  # 退貨是增加庫存

            # 更新當前庫存記錄
            update_query = """
                UPDATE Inventory
                SET product_code = %s, date = %s, status = %s, quantity = %s, current_stock = %s, notes = %s
                WHERE inventory_id = %s
            """
            self.cursor.execute(update_query, (product_code, date, status, quantity, update_current_stock, notes, inventory_id))
            self.connection.commit()

            # 調整從變動日期後的所有庫存記錄的 current_stock
            update_quantity = update_current_stock - current_stock
            print(f"{update_quantity}")
            print(f"{update_current_stock}")
            print(f"{current_stock}")
            if update_quantity > 0:
                print("到底是不是執行這邊? 這邊明明是+，我明明是負數為啥執行這邊")
                adjust_query = """
                    UPDATE Inventory
                    SET current_stock = current_stock + %s
                    WHERE product_code = %s AND date > %s
                """
            else:
                print("應該是要執行這邊才對啊")
                adjust_query = """
                    UPDATE Inventory
                    SET current_stock = current_stock + %s
                    WHERE product_code = %s AND date > %s
                """

            self.cursor.execute(adjust_query, (update_quantity, product_code, date))
            self.connection.commit()

        except mysql.connector.Error as err:
            print(f"Error adjusting inventory after date: {err}")

