# inventory_deduction_window.py
import os
from PyQt6.QtCore import pyqtSignal
from datetime import datetime
import time 
from PyQt6.QtWidgets import (QMainWindow, 
                             QTableWidget, 
                             QTableWidgetItem, 
                             QVBoxLayout,
                             QHBoxLayout, 
                             QWidget, 
                             QTabWidget, 
                             QDialog, 
                             QVBoxLayout, 
                             QTextEdit,
                             QPushButton,
                             QListWidget,
                             QListWidgetItem,
                             QMessageBox,
                             QFormLayout,
                             QComboBox,
                             QCompleter,
                             QDateTimeEdit,
                             QLineEdit
                             )
from PyQt6.QtCore import QDateTime,Qt,QDate

class InventoryDeductionWindow(QWidget):
    closed = pyqtSignal()

    def __init__(self, parent=None, order_all_data=None,folder_path=None,database=None):
        super().__init__(parent)
        self.order_all_data = order_all_data  # 儲存 processed_data
        self.folder_path=folder_path
        self.database=database
        self.setWindowTitle("庫存扣除處理視窗")
        self.setMinimumSize(300, 400)
        self.resize(500, 600)
        self.initialize_ui()
        self.create_table()

    def initialize_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        self.button_layout = QHBoxLayout()
      
        # 建立表格
        self.inventory_table = QTableWidget(self)
        self.display_layout.addWidget(self.inventory_table, 5)

        self.order_input_inventory_button = QPushButton("扣庫存", self)
        self.order_input_inventory_button.clicked.connect(self.order_input_inventory)  # 替換為實際存在的函數
        self.button_layout.addWidget(self.order_input_inventory_button)


        self.display_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.display_area)

    def create_table(self):
        self.all_product_codes = self.database.inventory_dao.get_all_product_codes()
        # 初始化表格
        self.inventory_table.setRowCount(0)
        self.inventory_table.setColumnCount(7)
        self.inventory_table.setHorizontalHeaderLabels(['物流', '商品代號', '數量', '單位', '前次庫存量', '庫存量', '庫存功能'])

        # 從 '總計資料' 擷取資料並填充表格
        if "總計資料" in self.order_all_data:
            if "通盈" in self.order_all_data["總計資料"]:
                self.fill_inventory_data("通盈", self.order_all_data["總計資料"]["通盈"])

            if "大榮" in self.order_all_data["總計資料"]:
                self.fill_inventory_data("大榮", self.order_all_data["總計資料"]["大榮"])

        # 自動調整列和行的大小
        self.inventory_table.resizeColumnsToContents()
        self.inventory_table.resizeRowsToContents()

    def fill_inventory_data(self, logistics_name, order_summary_data):
         for product_code, quantity in order_summary_data.items():
            row_count = self.inventory_table.rowCount()
            self.inventory_table.insertRow(row_count)
            
            # 填入物流名稱
            self.inventory_table.setItem(row_count, 0, QTableWidgetItem(logistics_name))
            # 填入商品代號
            self.inventory_table.setItem(row_count, 1, QTableWidgetItem(product_code))
            # 填入數量
            self.inventory_table.setItem(row_count, 2, QTableWidgetItem(str(quantity)))
            # 填入單位
            self.inventory_table.setItem(row_count, 3, QTableWidgetItem("箱"))

            # 填入前次庫存量
            second_latest_inventory_amount = self.database.inventory_dao.get_second_latest_inventory(product_code)
            second_latest_inventory_amount = second_latest_inventory_amount if second_latest_inventory_amount is not None else "無紀錄"
            self.inventory_table.setItem(row_count, 4, QTableWidgetItem(str(second_latest_inventory_amount)))

            # 填入庫存量
            inventory_amount = self.database.inventory_dao.get_latest_inventory(product_code)
            inventory_amount = inventory_amount if inventory_amount is not None else "無紀錄"
            self.inventory_table.setItem(row_count, 5, QTableWidgetItem(str(inventory_amount)))

            # 添加庫存功能按鈕
            inventory_button = QPushButton("庫存功能")
            inventory_button.clicked.connect(lambda _, r=row_count: self.add_inventory(r))
            self.inventory_table.setCellWidget(row_count, 6, inventory_button)
        # for product_code, quantity in inventory_data.items():
        #     # 插入新的一行
        #     self.inventory_table.insertRow(self.inventory_table.rowCount())

        #     # 填寫物流名稱
        #     self.inventory_table.setItem(self.inventory_table.rowCount() - 1, 0, QTableWidgetItem(logistics_name))

        #     # 填寫商品代號
        #     self.inventory_table.setItem(self.inventory_table.rowCount() - 1, 1, QTableWidgetItem(product_code))

        #     # 填寫數量
        #     self.inventory_table.setItem(self.inventory_table.rowCount() - 1, 2, QTableWidgetItem(str(quantity)))

        #     # 填寫單位為 '箱'
        #     self.inventory_table.setItem(self.inventory_table.rowCount() - 1, 3, QTableWidgetItem("箱"))
    
    def add_inventory(self, row_idx):
        dialog = QDialog(self)
        dialog.setWindowTitle("新增庫存變動")
        layout = QFormLayout(dialog)

        # 商品代號輸入框，帶有自動補全功能
        product_code_edit = QComboBox()
        product_code_edit.setEditable(True)
        product_code_edit.addItems(self.all_product_codes)
        # product_code_edit.setCompleter(QCompleter(self.all_product_codes))
        # 設定 QCompleter 並設定大小寫不敏感
        completer = QCompleter(self.all_product_codes)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        product_code_edit.setCompleter(completer)

        # 預填充商品代號
        item = self.inventory_table.item(row_idx, 1)
        item_1= self.inventory_table.item(row_idx, 0)
        if item:
            product_code_edit.setCurrentText(item.text())
        if item_1:
            item_1=item_1.text()

        # 日期時間輸入框，預設為當前日期和時間
        datetime_edit = QDateTimeEdit(calendarPopup=True)
        datetime_edit.setDateTime(QDateTime.currentDateTime())
        datetime_edit.setDisplayFormat('yyyy-MM-dd HH:mm')
        # 預設填入今天的日期 (MM/dd) 到備註框
        today_date = QDate.currentDate()
        today_date_str = today_date.toString('MM/dd')
        
        # 狀態選擇框
        status_edit = QComboBox()
        status_edit.addItems(["製造", "銷貨", "退貨", "瑕疵品"])

        quantity_edit = QLineEdit()

        # 備註輸入框
        notes_edit = QLineEdit()
        notes_edit.setText(f"{today_date_str} {item_1}")

        layout.addRow("商品代號", product_code_edit)
        layout.addRow("日期時間 (YYYY-MM-DD HH:MM)", datetime_edit)
        layout.addRow("狀態", status_edit)
        layout.addRow("數量", quantity_edit)
        layout.addRow("備註", notes_edit)  # 添加備註輸入框

        buttons = QHBoxLayout()
        add_button = QPushButton("新增")
        add_button.clicked.connect(lambda: self.save_inventory(
            dialog,
            None,
            product_code_edit.currentText(),  # 使用 currentText() 而不是 text()
            datetime_edit.dateTime().toString('yyyy-MM-dd HH:mm:ss'),
            status_edit.currentText(),  # 使用 currentText() 而不是 text()
            int(quantity_edit.text()),
            None,
            notes_edit.text()  # 傳遞備註的值,
        ))
        buttons.addWidget(add_button)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

        dialog.setLayout(layout)

        # 設定對話框大小
        dialog.resize(400, 150)  # 設定合適的寬度和高度

        dialog.exec()

    def save_inventory(self, dialog, inventory_id, product_code, date, status, quantity, current_stock, notes):
        if inventory_id is None:
            # 如果 inventory_id 为 None，则执行新增操作
            print("走這邊嗎????? 這便是新增商品庫存")
            self.database.inventory_dao.insert_inventory(product_code, date, status, quantity, notes)
        else:
            # 否则执行更新操作
            print("還是這邊??? 這邊是更新原有資料")
            self.database.inventory_dao.adjust_inventory_after_date(inventory_id, product_code, date, status, quantity, current_stock, notes)
            QMessageBox.information(self, "資訊", "庫存變動已更新")

        if dialog is not None:
            self.update_inventory_table(product_code)
            QMessageBox.information(self, "資訊", "庫存變動已新增")
            dialog.accept()
        else:
            self.update_inventory_table(product_code)



    def update_inventory_table(self, product_code):
        """
        更新表格中指定商品代號的庫存量。
        """
        # 遍歷表格的每一行，找到對應的商品代號，並更新其庫存量
        for row in range(self.inventory_table.rowCount()):
            table_product_code = self.inventory_table.item(row, 1).text()
            if table_product_code == product_code:
                inventory_amount_0 = self.database.inventory_dao.get_second_latest_inventory(product_code)
                inventory_amount_0 = inventory_amount_0 if inventory_amount_0 is not None else "無紀錄"
                self.inventory_table.setItem(row, 4, QTableWidgetItem(str(inventory_amount_0)))
                # 取得最新的庫存量
                inventory_amount = self.database.inventory_dao.get_latest_inventory(product_code)
                inventory_amount = inventory_amount if inventory_amount is not None else "無紀錄"
                # 更新庫存量到表格
                self.inventory_table.setItem(row, 5, QTableWidgetItem(str(inventory_amount)))
                break  # 更新後退出迴圈，避免不必要的疊代

    def order_input_inventory(self):
        """
        從表格中讀取每一行的資料，並扣除相應的庫存。
        在執行扣除之前，檢查是否已有相同的扣除記錄。
        """
        # 取得當前日期時間
        current_date_time = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')

        # 用來儲存要扣除的記錄
        records_to_deduct = []

        for row in range(self.inventory_table.rowCount()):
            # 取得商品代號
            product_code_item = self.inventory_table.item(row, 1)
            if not product_code_item:
                continue  # 如果商品代號不存在，跳過此行
            
            product_code = product_code_item.text()

            # 取得數量
            quantity_item = self.inventory_table.item(row, 2)
            if not quantity_item:
                continue  # 如果數量不存在，跳過此行
            
            quantity = int(quantity_item.text()) if quantity_item.text().isdigit() else 0

            # 取得物流名稱作為狀態
            logistics_item = self.inventory_table.item(row, 0)
            notes_logistics_item = logistics_item.text() if logistics_item else "未知"
            status = "銷貨"
            # 預設備註格式
            today_date_str = QDate.currentDate().toString('MM/dd')
            notes = f"{today_date_str} {notes_logistics_item}"

            # 收集待扣除的記錄
            records_to_deduct.append((product_code, status, quantity, notes))
        
        # 檢查是否有重複記錄
        for product_code, status, quantity, notes in records_to_deduct:
            # 取得最新庫存記錄
            latest_inventory_record = self.database.inventory_dao.get_latest_inventory_record(product_code)
            
            if latest_inventory_record:
                # 對比庫存記錄
                if (latest_inventory_record['status'] == status and
                    latest_inventory_record['quantity'] == quantity and
                    latest_inventory_record['notes'] == notes):
                    QMessageBox.warning(self, "警告", f"商品 {product_code} 的庫存已經被扣除過相同記錄，請檢查！")
                    return  # 退出方法，不執行扣除操作
        
        # 扣除庫存
        for product_code, status, quantity, notes in records_to_deduct:
            # 取得當前日期時間
            current_date_time = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')

            self.save_inventory(
                None,  # dialog 未使用
                None,  # inventory_id 為 None，執行新增操作
                product_code,
                current_date_time,
                status,
                quantity,  # 扣除庫存
                None,  # current_stock 未使用
                notes
            )
            # 在扣除庫存後顯示訊息
            print(f"商品 {product_code} 庫存已扣除 {quantity}")
            # 等待 1 秒鐘再進行下一個扣除
            time.sleep(1)

        QMessageBox.information(self, "完成", "所有庫存扣除已完成")
        # """
        # 從表格中讀取每一行的資料，並扣除相應的庫存。
        # """
        # # 取得當前日期時間
        # current_date_time = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mm:ss')

        # for row in range(self.inventory_table.rowCount()):
        #     # 取得商品代號
        #     product_code_item = self.inventory_table.item(row, 1)
        #     if not product_code_item:
        #         continue  # 如果商品代號不存在，跳過此行
            
        #     product_code = product_code_item.text()

        #     # 取得數量
        #     quantity_item = self.inventory_table.item(row, 2)
        #     if not quantity_item:
        #         continue  # 如果數量不存在，跳過此行
            
        #     quantity = int(quantity_item.text()) if quantity_item.text().isdigit() else 0

        #     # 取得物流名稱作為狀態
        #     logistics_item = self.inventory_table.item(row, 0)
        #     notes_logistics_item = logistics_item.text() if logistics_item else "未知"
        #     status="銷貨"
        #     # 預設備註格式
        #     today_date_str = QDate.currentDate().toString('MM/dd')
        #     notes = f"{today_date_str} {notes_logistics_item}"

        #     # 請求 save_inventory 方法來扣除庫存
        #     self.save_inventory(
        #         None,  # dialog 未使用
        #         None,  # inventory_id 為 None，執行新增操作
        #         product_code,
        #         current_date_time,
        #         status,
        #         quantity,  # 扣除庫存
        #         None,  # current_stock 未使用
        #         notes
        #     )

        #     # 在扣除庫存後顯示訊息
        #     print(f"商品 {product_code} 庫存已扣除 {quantity}")

        # QMessageBox.information(self, "完成", "所有庫存扣除已完成")

    def closeEvent(self, event):
        self.closed.emit()  # 當視窗關閉時發出訊號
        super().closeEvent(event)