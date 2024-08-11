# database_widget.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt6.QtCore import pyqtSignal
from success_login.database_widget.product_list_widget import ProductListWidget
from success_login.database_widget.inventory_widget import InventoryWidget
from success_login.database_widget.customer_information_widget import CustomerInformation


'''
資料庫功能，主要寫在這邊，我把各功能用物件導向的方式分包出去，所以會有上面的商品清單
跟庫存查詢
之後要再擴充客戶資料跟其他一些東西，我在思考，出貨功能要不要寫在這邊，還是說要再上一層
在擴充一個功能。

'''
class DatabaseWidget(QWidget):

    closed = pyqtSignal()

    def __init__(self, parent=None, database=None):
        super().__init__(parent)
        self.database = database
        self.setWindowTitle("庫存資料庫功能")
        self.setMinimumSize(900, 600)
        
        self.main_layout = QVBoxLayout(self)
        
        self.initialize_ui()
        
    def initialize_ui(self):
        self.button_layout = QHBoxLayout()
        
        self.product_table_button = QPushButton("商品清單")
        self.product_table_button.clicked.connect(self.show_product_list)
        self.button_layout.addWidget(self.product_table_button)
        
        self.inventory_button = QPushButton("庫存功能")
        self.inventory_button.clicked.connect(self.show_inventory_function)
        self.button_layout.addWidget(self.inventory_button)

        self.customer_information_button=QPushButton("客戶資料")
        self.customer_information_button.clicked.connect(self.show_customer_information)
        self.button_layout.addWidget(self.customer_information_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        self.main_layout.addWidget(self.display_area)

        # 初始化GridLayout對象(之後再做self.display_area，裡面物件布局時候，可能會用到，所以在這邊先設變數出來，方便保存他的物件，在後面清除時候才可以清掉)
        self.grid_layout = None
        self.table_widget = None
    
    def show_product_list(self):
        self.clear_display_area()
        self.product_list_widget = ProductListWidget(database=self.database)
        self.display_layout.addWidget(self.product_list_widget)
    
    def show_inventory_function(self):
        self.clear_display_area()
        self.inventory_widget = InventoryWidget(database=self.database)
        self.display_layout.addWidget(self.inventory_widget)


    def show_customer_information(self):
        self.clear_display_area()
        self.customer_information_widget =CustomerInformation(database=self.database)
        self.display_layout.addWidget(self.customer_information_widget)


    def clear_display_area(self):
        # 清空顯示區域
        while self.display_layout.count() > 0:
            item = self.display_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 清空GridLayout对象及其中的部件
        if self.grid_layout:
            while self.grid_layout.count() > 0:
                item = self.grid_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            # 將布局管理器置空，以便重新使用
            self.grid_layout = None

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

