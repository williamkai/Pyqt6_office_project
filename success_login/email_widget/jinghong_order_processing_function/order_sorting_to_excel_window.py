# order_sorting_window.py
import os
from PyQt6.QtCore import pyqtSignal
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.shared import RGBColor
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

class OrderSortingToExcelWindow(QWidget):

    closed = pyqtSignal()

    def __init__(self, parent=None, order_all_data=None,folder_path=None):
        super().__init__(parent)  # 僅傳遞 parent 參數給 QWidget
        self.order_all_data = order_all_data  # 儲存 processed_data
        self.folder_path=folder_path
        self.order_table = None
        self.stats=None
        self.setWindowTitle("銷貨明細處理視窗")
        self.setMinimumSize(300, 400)
        self.resize(400, 600)
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
        # 清空表格
        self.order_table.setRowCount(0)
        # 設定表頭
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(['物流','訂單來源', '商品代號', '數量', '單位'])
        # 填充資料
        row_count = 0
        # 處理"通盈"的資料
        if "通盈" in self.order_all_data["訂單資料"]:
            order_all_data = self.order_all_data["訂單資料"]["通盈"]
            
            logistics_filled = False  # 標記是否已填充物流
            for key, order in order_all_data.items():
                order_source_filled = False  # 標記是否已填充訂單來源
                for i, item in enumerate(order['items']):
                    self.order_table.insertRow(row_count)
                    
                    if not logistics_filled:
                        # 在第一行填寫物流
                        self.order_table.setItem(row_count, 0, QTableWidgetItem("通盈"))
                        logistics_filled = True
                    else:
                        self.order_table.setItem(row_count, 0, QTableWidgetItem(""))
                    
                    if not order_source_filled:
                        # 在第一行填寫訂單來源
                        self.order_table.setItem(row_count, 1, QTableWidgetItem(order['title']))
                        order_source_filled = True
                    else:
                        self.order_table.setItem(row_count, 1, QTableWidgetItem(""))

                    # 填寫商品代號、數量和單位
                    self.order_table.setItem(row_count, 2, QTableWidgetItem(item['product_code']))
                    self.order_table.setItem(row_count, 3, QTableWidgetItem(item['quantity']))
                    self.order_table.setItem(row_count, 4, QTableWidgetItem("箱"))
                    
                    row_count += 1

        # 處理“大榮”的資料
        if "大榮" in self.order_all_data["訂單資料"]:
            order_all_data = self.order_all_data["訂單資料"]["大榮"]
            
            logistics_filled = False  # 標記是否已填充物流
            for key, order in order_all_data.items():
                order_source_filled = False  # 標記是否已填充訂單來源
                for i, item in enumerate(order['items']):
                    self.order_table.insertRow(row_count)
                    
                    if not logistics_filled:
                        # 在第一行填寫物流
                        self.order_table.setItem(row_count, 0, QTableWidgetItem("大榮"))
                        logistics_filled = True
                    else:
                        self.order_table.setItem(row_count, 0, QTableWidgetItem(""))
                    
                    if not order_source_filled:
                        # 在第一行填寫訂單來源
                        self.order_table.setItem(row_count, 1, QTableWidgetItem(order['title']))
                        order_source_filled = True
                    else:
                        self.order_table.setItem(row_count, 1, QTableWidgetItem(""))

                    # 填寫商品代號、數量和單位
                    self.order_table.setItem(row_count, 2, QTableWidgetItem(item['product_code']))
                    self.order_table.setItem(row_count, 3, QTableWidgetItem(item['quantity']))
                    self.order_table.setItem(row_count, 4, QTableWidgetItem("箱"))
                    
                    row_count += 1
        # # 處理"通盈"的資料
        # if "通盈" in self.order_all_data["訂單資料"]:
        #     order_all_data = self.order_all_data["訂單資料"]["通盈"]
            
        #     for key, order in order_all_data.items():
        #         for i, item in enumerate(order['items']):
        #             self.order_table.insertRow(row_count)
                    
        #             if i == 0:
        #                 # 填寫物流和訂單來源
        #                 self.order_table.setItem(row_count, 0, QTableWidgetItem("通盈"))
        #                 self.order_table.setItem(row_count, 1, QTableWidgetItem(order['title']))
        #             else:
        #                 # 填寫物流和訂單來源空白
        #                 self.order_table.setItem(row_count, 0, QTableWidgetItem(""))
        #                 self.order_table.setItem(row_count, 1, QTableWidgetItem(""))

        #             # 填寫商品代號、數量和單位
        #             self.order_table.setItem(row_count, 2, QTableWidgetItem(item['product_code']))
        #             self.order_table.setItem(row_count, 3, QTableWidgetItem(item['quantity']))
        #             self.order_table.setItem(row_count, 4, QTableWidgetItem("箱"))
                    
        #             row_count += 1

        # # 處理“大榮”的資料
        # if "大榮" in self.order_all_data["訂單資料"]:
        #     order_all_data = self.order_all_data["訂單資料"]["大榮"]
            
        #     for key, order in order_all_data.items():
        #         for i, item in enumerate(order['items']):
        #             self.order_table.insertRow(row_count)
                    
        #             if i == 0:
        #                 # 填寫物流和訂單來源
        #                 self.order_table.setItem(row_count, 0, QTableWidgetItem("大榮"))
        #                 self.order_table.setItem(row_count, 1, QTableWidgetItem(order['title']))
        #             else:
        #                 # 填寫物流和訂單來源空白
        #                 self.order_table.setItem(row_count, 0, QTableWidgetItem(""))
        #                 self.order_table.setItem(row_count, 1, QTableWidgetItem(""))

        #             # 填寫商品代號、數量和單位
        #             self.order_table.setItem(row_count, 2, QTableWidgetItem(item['product_code']))
        #             self.order_table.setItem(row_count, 3, QTableWidgetItem(item['quantity']))
        #             self.order_table.setItem(row_count, 4, QTableWidgetItem("箱"))
                    
        #             row_count += 1
        
        # 調整表格顯示
        self.order_table.resizeColumnsToContents()
        self.order_table.resizeRowsToContents()
            
        print(f"關查字典長相:\n{self.order_all_data}")
        print(f"選擇key後的訂單長相:\n{order_all_data}")
        print("建立表格")

    def input_table_to_excel(slef):
        print("這個會是把資料寫進excel")




    def closeEvent(self, event):
        self.closed.emit()  # 當視窗關閉時發出訊號
        super().closeEvent(event)