from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QApplication)
from PyQt6.QtCore import Qt
class SplitLayoutExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Split Layout Example')
        self.setGeometry(100, 100, 800, 600)
        self.initialize_ui()

    def initialize_ui(self):
        main_layout = QVBoxLayout(self)

        # 上部区域 (Top section)
        top_layout = QHBoxLayout()
        top_left_label = QLabel('Top Left', self)
        top_right_label = QLabel('Top Right', self)
        top_right_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        top_layout.addWidget(top_left_label)
        top_layout.addWidget(top_right_label)

        top_widget = QWidget()
        top_widget.setLayout(top_layout)

        # 中部区域 (Middle section)
        middle_table = QTableWidget(5, 3, self)
        middle_table.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])
        for row in range(5):
            for col in range(3):
                middle_table.setItem(row, col, QTableWidgetItem(f'Item {row+1}-{col+1}'))

        # 下部区域 (Bottom section)
        bottom_layout = QGridLayout()
        bottom_label1 = QLabel('Bottom Label 1', self)
        bottom_label2 = QLabel('Bottom Label 2', self)
        bottom_button = QPushButton('Bottom Button', self)
        bottom_layout.addWidget(bottom_label1, 0, 0)
        bottom_layout.addWidget(bottom_label2, 0, 1)
        bottom_layout.addWidget(bottom_button, 1, 0, 1, 2)  # Button spans across two columns

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_layout)

        # 将上、中、下区域添加到主布局
        main_layout.addWidget(top_widget)
        main_layout.addWidget(middle_table)
        main_layout.addWidget(bottom_widget)

if __name__ == '__main__':
    app = QApplication([])
    window = SplitLayoutExample()
    window.show()
    app.exec()





"""下面是暫時放的"""

def create_sales_order_table(self):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS SalesOrder (
            order_id VARCHAR(255) PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL,
            order_date DATETIME NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            status ENUM('已完成', '待出貨', '已取消') NOT NULL
        )
    """
    # 執行創建表的SQL語句

def create_sales_order_detail_table(self):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS SalesOrderDetail (
            detail_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id VARCHAR(255) NOT NULL,
            product_code VARCHAR(255) NOT NULL,
            quantity INT NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES SalesOrder(order_id),
            FOREIGN KEY (product_code) REFERENCES ProductList(product_code)
        )
    """
    # 執行創建表的SQL語句

def generate_order_id(self, db_connection):
    from datetime import datetime
    today = datetime.now().strftime('%Y%m%d')
    
    cursor = db_connection.cursor()
    query = """
        SELECT order_id FROM SalesOrder
        WHERE order_id LIKE %s
        ORDER BY order_id DESC
        LIMIT 1
    """
    cursor.execute(query, (today + '%',))
    result = cursor.fetchone()
    
    if result:
        latest_order_id = result[0]
        latest_sequence = int(latest_order_id[-4:])
        new_sequence = latest_sequence + 1
    else:
        new_sequence = 1
    
    new_order_id = f"{today}{new_sequence:04d}"
    return new_order_id



"""再次更改"""
def create_sales_order_table(self):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS SalesOrder (
            order_id VARCHAR(255) PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL,
            order_date DATETIME NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (customer_name) REFERENCES CustomerList(customer_name)
        )
    """


def create_sales_order_detail_table(self):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS SalesOrderDetail (
            detail_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id VARCHAR(255) NOT NULL,
            product_code VARCHAR(255) NOT NULL,
            quantity INT NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            notes TEXT DEFAULT NULL,
            FOREIGN KEY (order_id) REFERENCES SalesOrder(order_id),
            FOREIGN KEY (product_code) REFERENCES ProductList(product_code)
        )
    """
"""這是我要的客戶訂單，最後要的~~"""
def create_sales_order_table(self):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS SalesOrder (
            order_id VARCHAR(255) PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL,
            order_date DATETIME NOT NULL,
            total_amount DECIMAL(10, 2) DEFAULT NULL,
            status ENUM('已完成', '待出貨', '已取消') NOT NULL,
            settled ENUM('已結帳', '未結帳') NOT NULL,
            FOREIGN KEY (company_name) REFERENCES Customers(CompanyName)
        )
    """


def create_sales_order_table(self):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS SalesOrder (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id VARCHAR(255) UNIQUE NOT NULL,
            company_name VARCHAR(255) NOT NULL,
            order_date DATETIME NOT NULL,
            total_amount DECIMAL(10, 2) DEFAULT NULL,
            status ENUM('已完成', '待出貨', '已取消') NOT NULL,
            settled ENUM('已結帳', '未結帳') NOT NULL,
            FOREIGN KEY (company_name) REFERENCES Customers(CompanyName)
        )
    """

def create_sales_order_detail_table(self):
    create_table_query = """
        CREATE TABLE IF NOT EXISTS SalesOrderDetail (
            detail_id INT AUTO_INCREMENT PRIMARY KEY,
            order_id VARCHAR(255) NOT NULL,
            product_code VARCHAR(255) NOT NULL,
            quantity INT NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            notes TEXT DEFAULT NULL,
            FOREIGN KEY (order_id) REFERENCES SalesOrder(order_id),
            FOREIGN KEY (product_code) REFERENCES ProductList(product_code)
        )
    """
