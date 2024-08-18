# order_sorting_window.py
import os
from PyQt6.QtCore import pyqtSignal
from docx import Document
from datetime import datetime
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
                             QListWidgetItem)

class OrderSortingWindow(QWidget):
    closed = pyqtSignal()
    data_changed = pyqtSignal(dict)

    def __init__(self, parent=None, processed_data=None,folder_path=None):
        super().__init__(parent)  # 僅傳遞 parent 參數給 QWidget
        self.processed_data = processed_data  # 儲存 processed_data
        self.folder_path=folder_path
        self.order_list = None
        self.order_table = None
        self.setWindowTitle("訂單處理結果")
        self.setMinimumSize(300, 400)
        self.resize(600, 400)
        self.initialize_ui()
        self.create_order_list()

    def initialize_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        
        # 如果 order_list 尚未建立，則建立它
        if self.order_list is None:
            self.order_list = QListWidget(self)
            self.order_list.setMinimumHeight(50)
            self.order_list.itemClicked.connect(self.display_order_table)
            self.display_layout.addWidget(self.order_list, 1)
                
        # 建立表格
        if self.order_table is None:
            self.order_table = QTableWidget(self)
            self.display_layout.addWidget(self.order_table, 6)
        
        save_button = QPushButton("Save to Word", self)
        save_button.clicked.connect(self.save_table_to_word)  # 連結按鈕點擊事件到儲存功能
        self.display_layout.addWidget(save_button)  # 將按鈕添加到佈局中
        
        self.main_layout.addWidget(self.display_area)

    def create_order_list(self):
        self.order_list.clear()  # 清空之前的郵件列表
        order_list_title = ["大榮", "通盈"]
        for title in order_list_title:
            item = QListWidgetItem(title)  # 使用 title 替代 "tilte"
            self.order_list.addItem(item)

    def display_order_table(self):
    # 清空表格
        self.order_table.clear()

        # 取得選中的列表項
        selected_item = self.order_list.currentItem()
        if not selected_item:
            return

        # 根據選中的項的文本來取得相應的資料
        selected_key = selected_item.text()

        # 從 processed_data 中擷取相應的資料
        data_to_display = self.processed_data.get(selected_key, {})

        # 顯示表格
        self.create_order_table(data_to_display)

    def create_order_table(self, data):
        # 轉換鍵爲字串
        data = self.convert_keys_to_str(data)
        
        # 清空表格
        self.order_table.setRowCount(0)
        
        # 設定表頭
        self.order_table.setColumnCount(4)
        self.order_table.setHorizontalHeaderLabels(['訂單來源', '商品代號', '數量', '單位'])

        # 填充資料
        row_count = 0
        for key, order in data.items():
            for i, item in enumerate(order['items']):
                self.order_table.insertRow(row_count)
                if i == 0:
                    self.order_table.setItem(row_count, 0, QTableWidgetItem(order['title']))
                self.order_table.setItem(row_count, 1, QTableWidgetItem(item['product_code']))
                self.order_table.setItem(row_count, 2, QTableWidgetItem(item['quantity']))
                self.order_table.setItem(row_count, 3, QTableWidgetItem('箱'))
                row_count += 1

        # 調整表格顯示
        self.order_table.resizeColumnsToContents()
        self.order_table.resizeRowsToContents()

    def convert_keys_to_str(self, data):
        if isinstance(data, dict):
            return {k.decode('utf-8') if isinstance(k, bytes) else k: self.convert_keys_to_str(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_keys_to_str(i) for i in data]
        else:
            return data

    def save_changes(self):
        # 根據表格中的資料產生字典
        modified_data = self.generate_data_from_table()
        self.data_changed.emit(modified_data)  # 發送資料
        self.close()  # 關閉視窗
    
    def generate_data_from_table(self):
        # 根據表格資料產生字典的邏輯
        return {}
    
    def save_table_to_word(self):
        selected_item = self.order_list.currentItem()
        if not selected_item:
            return  # 如果沒有選擇的項目，則不進行任何操作

        if self.folder_path is None:
            print("Error: folder_path is not set.")
            return

        # 確保 folder_path 使用適當的分隔符
        if not self.folder_path.endswith(os.path.sep):
            self.folder_path += os.path.sep
        # 建立 Word 文件
        doc = Document()
        
        # 設定標題
        # doc.add_heading(f'{selected_item.text()}', level=1)
        
        # 擷取表格資料
        row_count = self.order_table.rowCount()
        col_count = self.order_table.columnCount()

        previous_title = None
        selected_item_1=selected_item.text()

        for row in range(row_count):
            title = self.order_table.item(row, 0).text() if self.order_table.item(row, 0) else ''
            product_code = self.order_table.item(row, 1).text() if self.order_table.item(row, 1) else ''
            quantity = self.order_table.item(row, 2).text() if self.order_table.item(row, 2) else ''
            unit = self.order_table.item(row, 3).text() if self.order_table.item(row, 3) else ''
            
            # 如果第一欄有值，添加到 Word 文件中
            if title:
                if previous_title:
                    doc.add_paragraph()  # 空一行

                if selected_item_1 =='大榮': 
                    doc.add_paragraph(f"{title} 大榮-久富餘-菁弘")
                    previous_title = title
                elif selected_item_1 =="通盈":
                    doc.add_paragraph(f"{title} 通盈-久富餘-菁弘")
                    previous_title = title


            # 添加商品資料
            doc.add_paragraph(f"{product_code}......{quantity}{unit}")

        # 儲存 Word 文件到指定路徑
        # 儲存 Word 文件到指定路徑
        # 取得當前日期
        today_date = datetime.now().strftime('%m%d')
        year = int(datetime.now().strftime('%Y'))
        year_TW = year - 1911
        today_date_tw=f"{year_TW}{today_date}"
        # 設定文件名稱
        # file_name = f'{today_date}{selected_item.text()}.docx'

        file_name = f'{today_date_tw}{selected_item.text()}.docx'
        file_path = os.path.join(self.folder_path, file_name)
        doc.save(file_path)
        print(f"File saved to {file_path}")

    def closeEvent(self, event):
        self.closed.emit()  # 當視窗關閉時發出訊號
        super().closeEvent(event)