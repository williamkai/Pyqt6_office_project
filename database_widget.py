from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QTextEdit
import pandas as pd
import mysql.connector

class DatabaseWidget(QWidget):

    closed = pyqtSignal()

    def __init__(self, parent=None, database=None):
        super().__init__(parent)
        self.database = database
        self.setWindowTitle("庫存資料庫功能")
        self.setMinimumSize(800, 600)
        
        self.main_layout = QVBoxLayout(self)
        
        # 上排的水平排列按鈕
        self.button_layout = QHBoxLayout()
        
        self.create_product_button = QPushButton("建立商品基本資料")
        self.create_product_button.clicked.connect(self.create_product)
        self.button_layout.addWidget(self.create_product_button)
        
        self.inventory_button = QPushButton("庫存功能")
        self.inventory_button.clicked.connect(self.inventory_function)
        self.button_layout.addWidget(self.inventory_button)
        
        self.product_table_button = QPushButton("商品總表")
        self.product_table_button.clicked.connect(self.product_table)
        self.button_layout.addWidget(self.product_table_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        # 顯示區域
        self.display_area = QTextEdit()
        self.display_area.setReadOnly(True)
        self.main_layout.addWidget(self.display_area)

    def create_product(self):
        self.display_area.clear()
        self.display_area.append("點擊建立商品基本資料")
        # 在這裡可以加上建立商品資料表的邏輯
        self.display_area.append("商品基本資料已建立")

    def inventory_function(self):
        self.display_area.clear()
        self.display_area.append("點擊庫存功能")
        # 在這裡可以加上庫存功能的邏輯
        self.display_area.append("庫存功能正在開發中")

    def product_table(self):
        self.display_area.clear()
        self.display_area.append("點擊商品總表")
        # 在這裡可以加上顯示商品總表的邏輯
        self.display_area.append("商品總表資料顯示")

    def load_data_to_pandas(self):
        print("先看看跑不跑的到")

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
