from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,QLineEdit

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
        
        # 顯示區域，使用QWidget
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        self.main_layout.addWidget(self.display_area)

    def create_product(self):
        self.clear_display_area()
        
        # 在顯示區域內加入標籤、輸入框、提交按鈕等
        label = QLabel("商品名稱:")
        self.display_layout.addWidget(label)
        
        line_edit = QLineEdit()
        self.display_layout.addWidget(line_edit)
        

        
        submit_button = QPushButton("提交")
        submit_button.setFixedSize(200, 40)
        submit_button.clicked.connect(lambda: self.submit_product(line_edit.text()))
        self.display_layout.addWidget(submit_button)

    def inventory_function(self):
        self.clear_display_area()
        
        # 在顯示區域內加入庫存功能相關的小部件
        label = QLabel("庫存功能正在開發中...")
        self.display_layout.addWidget(label)

    def product_table(self):
        self.clear_display_area()
        
        # 在顯示區域內顯示商品總表資料
        label = QLabel("商品總表資料顯示區域...")
        self.display_layout.addWidget(label)

    def clear_display_area(self):
        # 清空顯示區域
        for i in reversed(range(self.display_layout.count())):
            widget = self.display_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def submit_product(self, product_name):
        # 提交商品名稱等資料的處理
        self.clear_display_area()
        label = QLabel(f"已提交商品名稱: {product_name}")
        self.display_layout.addWidget(label)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()