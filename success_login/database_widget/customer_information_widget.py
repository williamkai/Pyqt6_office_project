# customer_information_widget.py
from PyQt6.QtWidgets import (QWidget, 
                             QVBoxLayout, 
                             QHBoxLayout, 
                             QPushButton, 
                             QLineEdit, 
                             QTableWidget, 
                             QTableWidgetItem, 
                             QMessageBox, QDialog, 
                             QFormLayout, 
                             QComboBox)
'''
客戶資料建檔
痾痾痾痾，這邊處理到一半，發現需要把dao，重新設計，因為原本的方式會造成
成功登入後處理資料庫的程序越來越大包，所以要把本來的處理邏輯重新處理，
讓dao也把它做成物件導向的方式。
'''


class CustomerInformation(QWidget):
    
    def __init__(self, parent=None, database=None):
        print("客戶資料建檔的物件顯示窗")
        super().__init__(parent)
        self.database = database
        self.initialize_ui()

    def initialize_ui(self):
        self.layout = QVBoxLayout(self)
        self.customer_information_table()

    # def customer_information_table():
    #     self.clear_layout()
    #     self

        

    def clear_layout(self):
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


