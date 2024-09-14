# sales_widget.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt6.QtCore import pyqtSignal
from success_login.database_widget.product_list_widget import ProductListWidget
from success_login.database_widget.inventory_widget import InventoryWidget
from success_login.database_widget.customer_information_widget import CustomerInformation
from success_login.sales_widget.order_data_widget import OrderDataWidget
from success_login.sales_widget.sales_function_widget import SalesFunctionWidget

'''
銷貨功能

'''
class SalesWidget(QWidget):

    closed = pyqtSignal()

    def __init__(self, parent=None, database=None):
        super().__init__(parent)
        self.database = database
        self.setWindowTitle("銷貨訂單功能")
        self.setMinimumSize(900, 600)
        
        self.main_layout = QVBoxLayout(self)
        
        self.initialize_ui()
        
    def initialize_ui(self):
        self.button_layout = QHBoxLayout()
        
        self.order_query_button = QPushButton("查詢")
        self.order_query_button.clicked.connect(self.show_order_data)
        self.button_layout.addWidget(self.order_query_button)
        
        self.sales_function_button = QPushButton("銷貨功能")
        self.sales_function_button.clicked.connect(self.show_sales_function)
        self.button_layout.addWidget(self.sales_function_button)

        self.count_report_button=QPushButton("結算功能")
        self.count_report_button.clicked.connect(self.show_count_report)
        self.button_layout.addWidget(self.count_report_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        self.main_layout.addWidget(self.display_area)

        # 初始化GridLayout對象(之後再做self.display_area，裡面物件布局時候，可能會用到，所以在這邊先設變數出來，方便保存他的物件，在後面清除時候才可以清掉)
        self.grid_layout = None
        self.table_widget = None
    
    def show_order_data(self):
        self.clear_display_area()
        print("正在寫code")
        self.order_data_widget = OrderDataWidget(parent=self,database=self.database)
        self.display_layout.addWidget(self.order_data_widget)
    
    def show_sales_function(self):
        self.clear_display_area()
        self.sales_function_widget = SalesFunctionWidget(parent=self,database=self.database)
        self.display_layout.addWidget(self.sales_function_widget)
        print("銷貨功能表_還在寫")


    def show_count_report(self):
        self.clear_display_area()
        print("正在寫")


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

