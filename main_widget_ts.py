import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QPainter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = QTextEdit()
        self.print_button = QPushButton("Print")

        self.print_button.clicked.connect(self.print_text)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.print_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.setWindowTitle("Print Example")
        self.resize(400, 300)

    def print_text(self):
        # Create a QPrinter object with default settings
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        # Create a QPrintDialog to allow the user to select printer and settings
        print_dialog = QPrintDialog(printer, self)

        if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
            # Print the text document from QTextEdit
            self.text_edit.document().print(printer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())





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
