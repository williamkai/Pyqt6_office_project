# order_sorting_window.py
import os
from PyQt6.QtCore import pyqtSignal
from datetime import datetime
from openpyxl import load_workbook
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

class OrderSortingToExcelWindow(QWidget):
    START_ROW = 7
    SHEET_NAME = '工作表1'  # 可以根据实际情况修改
    FILE_NAME = "113年8月久富餘對帳明細表-菁弘(含退貨).xlsx"  # 文件名常量

    closed = pyqtSignal()

    def __init__(self, parent=None, order_all_data=None,folder_path=None):
        super().__init__(parent)  # 僅傳遞 parent 參數給 QWidget
        self.order_all_data = order_all_data  # 儲存 processed_data
        self.folder_path=folder_path
        self.order_table = None
        self.stats=None
        self.setWindowTitle("銷貨明細處理視窗")
        self.setMinimumSize(300, 400)
        self.resize(500, 600)
        self.initialize_ui()
        self.create_table()

    def initialize_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        self.but_layout =QHBoxLayout()
      
        # 建立表格
        if self.order_table is None:
            self.order_table = QTableWidget(self)
            self.display_layout.addWidget(self.order_table, 5)
        
        self.input_button = QPushButton("Input to Excel", self)
        self.input_button.clicked.connect(self.input_table_to_excel)  # 連結按鈕點擊事件到儲存功能
        self.but_layout.addWidget(self.input_button)
        self.display_layout.addLayout(self.but_layout)  # 將按鈕添加到佈局中
        
        self.main_layout.addWidget(self.display_area)

    def create_table(self):
        self.order_table.setRowCount(0)
        self.order_table.setColumnCount(6)
        self.order_table.setHorizontalHeaderLabels(['物流','訂單來源','出貨單號', '商品代號', '數量', '單位'])
        
        if "通盈" in self.order_all_data["訂單資料"]:
            self.fill_order_data("通盈", self.order_all_data["訂單資料"]["通盈"])
        
        if "大榮" in self.order_all_data["訂單資料"]:
            self.fill_order_data("大榮", self.order_all_data["訂單資料"]["大榮"])

        self.order_table.resizeColumnsToContents()
        self.order_table.resizeRowsToContents()

    def fill_order_data(self, logistics_name, order_all_data):
        logistics_filled = False
        for key, order in order_all_data.items():
            order_source_filled = False
            for i, item in enumerate(order['items']):
                self.order_table.insertRow(self.order_table.rowCount())
                
                if not logistics_filled:
                    self.order_table.setItem(self.order_table.rowCount()-1, 0, QTableWidgetItem(logistics_name))
                    logistics_filled = True
                else:
                    self.order_table.setItem(self.order_table.rowCount()-1, 0, QTableWidgetItem(""))

                if not order_source_filled:
                    self.order_table.setItem(self.order_table.rowCount()-1, 1, QTableWidgetItem(order['title']))
                    order_source_filled = True
                else:
                    self.order_table.setItem(self.order_table.rowCount()-1, 1, QTableWidgetItem(""))

                self.order_table.setItem(self.order_table.rowCount()-1, 3, QTableWidgetItem(item['product_code']))
                self.order_table.setItem(self.order_table.rowCount()-1, 4, QTableWidgetItem(item['quantity']))
                self.order_table.setItem(self.order_table.rowCount()-1, 5, QTableWidgetItem("箱"))
     
    def input_table_to_excel(self):
        # 确保表格有行数据
        if self.order_table.rowCount() == 0:
            print("表格沒有資料")
            return
    
        input_row_data = self.get_table_data()

        for data in input_row_data:
            print(f"全部的資料\n{data}")
        
        # 使用類屬性常數
        folder_path = os.path.join(self.folder_path, "菁弘明細")
        file_path = os.path.join(folder_path, self.FILE_NAME)

        try:
            wb = load_workbook(file_path)
            ws = wb[self.SHEET_NAME]  # 使用常數 SHEET_NAME
        except FileNotFoundError:
            print(f"文件 {file_path} 未找到")
            return
        except Exception as e:
            print(f"無法打開文件: {e}")
            return

        # 從 START_ROW 開始搜尋空行
        first_empty_row = None
        for row in range(self.START_ROW, ws.max_row + 1):  # ws.max_row 为现有行数
            if ws.cell(row, 4).value is None:  # 检查 D 列（索引 4），注意 openpyxl 的索引从 1 开始
                first_empty_row = row
                break

        if first_empty_row is None:
            first_empty_row = ws.max_row + 1

        # 寫入資料
        for i, row_data in enumerate(input_row_data):
            row_index = first_empty_row + i

            if row_data[0]:  # 如果第一列数据非空
                ws.cell(row_index, 1, datetime.now().strftime("%Y/%m/%d")) 
            if len(row_data) > 0:
                ws.cell(row_index, 2, row_data[0])  
            if len(row_data) > 1:
                ws.cell(row_index, 3, row_data[1])  
            if len(row_data) > 2:
                ws.cell(row_index, 4, row_data[2])  
            if len(row_data) > 3:
                ws.cell(row_index, 7, row_data[3]) 
        try:
            wb.save(file_path)
            print("資料已成功寫入 Excel 文件")
        except Exception as e:
            print(f"無法儲存文件: {e}")
            
    def get_table_data(self):
        input_row_data = []
        temp_value = ""
        resuper = ["JFS303001-01", "JTS101010-01", "JTS102004-01", "JTS151205-01", "TTS151406-01", "JTS151206-01"]

        for row in range(self.order_table.rowCount()):
            row_data = []
            for col in range(4):
                actual_col = col + 1
                item = self.order_table.item(row, actual_col)
                cell_text = item.text() if item else ""

                if actual_col == 2:
                    if cell_text:
                        temp_value = cell_text
                    row_data.append(temp_value)
                elif actual_col == 3:
                    if cell_text in resuper:
                        cell_text += '.'
                    row_data.append(cell_text)
                else:
                    row_data.append(cell_text)

            input_row_data.append(row_data)
        return input_row_data

    def closeEvent(self, event):
        self.closed.emit()  # 當視窗關閉時發出訊號
        super().closeEvent(event)