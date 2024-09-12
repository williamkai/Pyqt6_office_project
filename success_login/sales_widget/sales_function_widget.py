# sales_function_widget.py
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QTableWidget)
from PyQt6.QtCore import Qt,QRect
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QPainter

class SalesFunctionWidget(QWidget):
    def __init__(self, parent=None, database=None):
        super().__init__(parent)
        self.database = database
        self.parent_widget = parent
        self.initialize_ui()

    def initialize_ui(self):
        print("北爛ㄚㄚㄚ 有夠討厭 超不會設計版面")
    #     # Main layout
    #     main_layout = QVBoxLayout(self)

    #     # Upper section (Top section + Customer info)
    #     self.upper_section = QWidget()
    #     self.upper_section.setStyleSheet("background-color: #f0f0f0;")
    #     self.upper_section.setGeometry(QRect(0, 0, 800, 200))  # Example size, adjust as needed

    #     # Create an absolute layout
    #     self.upper_section_layout = QVBoxLayout(self.upper_section)
    #     self.upper_section_layout.setContentsMargins(10, 10, 10, 10)

    #     # Company info
    #     company_info_layout = QGridLayout()
    #     company_info_layout.setContentsMargins(0, 0, 0, 0)

    #     self.company_name_label = QLabel("公司名稱")
    #     self.company_name_label.setStyleSheet("font-size: 24px; font-weight: bold;")
    #     self.company_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #     self.company_name_label.setFixedSize(300, 40)  # Fixed size for better layout control
    #     company_info_layout.addWidget(self.company_name_label, 0, 0, 1, 2)

    #     self.phone_label = QLabel("電話: 04-8859467")
    #     self.phone_label.setFixedWidth(150)
    #     self.fax_label = QLabel("傳真: 04-8859468")
    #     self.fax_label.setFixedWidth(150)
    #     self.company_address_label = QLabel("地址: 彰化縣鹿港鎮東勢里鹿工南")
    #     self.company_address_label.setFixedWidth(150)
    #     company_info_layout.addWidget(self.phone_label, 0, 2, Qt.AlignmentFlag.AlignRight)
    #     company_info_layout.addWidget(self.fax_label, 1, 2, Qt.AlignmentFlag.AlignRight)
    #     company_info_layout.addWidget(self.company_address_label, 2, 2, Qt.AlignmentFlag.AlignRight)

    #     self.upper_section_layout.addLayout(company_info_layout)

    #     # Shipping note title
    #     self.shipping_title_layout = QGridLayout()
    #     self.shipping_title_label = QLabel("出貨單")
    #     self.shipping_title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
    #     self.shipping_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #     self.shipping_title_label.setFixedSize(300, 40)  # Fixed size for better layout control
    #     self.shipping_title_layout.addWidget(self.shipping_title_label, 0, 0, 1, 2)

    #     self.invoice_number_label = QLabel("憑單編號: ")
    #     self.invoice_number_label.setFixedWidth(100)
    #     self.shipping_title_layout.addWidget(self.invoice_number_label, 0, 2, Qt.AlignmentFlag.AlignRight)
    #     self.invoice_number_input = QLineEdit()
    #     self.invoice_number_input.setFixedWidth(150)
    #     self.shipping_title_layout.addWidget(self.invoice_number_input, 0, 3)

    #     self.upper_section_layout.addLayout(self.shipping_title_layout)

    #     # Customer and other info
    #     customer_info_layout = QGridLayout()
    #     customer_info_layout.setContentsMargins(0, 0, 0, 0)

    #     labels_width = 100
    #     inputs_width = 150

    #     self.customer_info_layout = customer_info_layout

    #     self.customer_info_layout.addWidget(QLabel("客戶名稱:"), 0, 0)
    #     self.customer_name_input = QLineEdit()
    #     self.customer_name_input.setFixedWidth(inputs_width)
    #     self.customer_info_layout.addWidget(self.customer_name_input, 0, 1)
        
    #     self.customer_info_layout.addWidget(QLabel("聯絡人:"), 1, 0)
    #     self.contact_person_input = QLineEdit()
    #     self.contact_person_input.setFixedWidth(inputs_width)
    #     self.customer_info_layout.addWidget(self.contact_person_input, 1, 1)
        
    #     self.customer_info_layout.addWidget(QLabel("統一編號:"), 2, 0)
    #     self.tax_id_input = QLineEdit()
    #     self.tax_id_input.setFixedWidth(inputs_width)
    #     self.customer_info_layout.addWidget(self.tax_id_input, 2, 1)
        
    #     self.customer_info_layout.addWidget(QLabel("電話:"), 2, 2)
    #     self.phone_input = QLineEdit()
    #     self.phone_input.setFixedWidth(inputs_width)
    #     self.customer_info_layout.addWidget(self.phone_input, 2, 3)
        
    #     self.customer_info_layout.addWidget(QLabel("日期:"), 2, 4)
    #     self.date_input = QLineEdit()
    #     self.date_input.setFixedWidth(inputs_width)
    #     self.customer_info_layout.addWidget(self.date_input, 2, 5)
        
    #     self.customer_info_layout.addWidget(QLabel("公司地址:"), 3, 0)
    #     self.company_address_input = QLineEdit()
    #     self.company_address_input.setFixedWidth(inputs_width)
    #     self.customer_info_layout.addWidget(self.company_address_input, 3, 1)
        
    #     self.customer_info_layout.addWidget(QLabel("發票號碼:"), 3, 2)
    #     self.invoice_number_input = QLineEdit()
    #     self.invoice_number_input.setFixedWidth(inputs_width)
    #     self.customer_info_layout.addWidget(self.invoice_number_input, 3, 3)
        
    #     self.customer_info_layout.addWidget(QLabel("指送地址:"), 4, 0)
    #     self.delivery_address_input = QLineEdit()
    #     self.delivery_address_input.setFixedWidth(inputs_width)
    #     self.customer_info_layout.addWidget(self.delivery_address_input, 4, 1)
        
    #     self.customer_info_layout.addWidget(QLabel("業務員:"), 4, 2)
    #     self.salesperson_input = QLineEdit()
    #     self.salesperson_input.setFixedWidth(inputs_width)
    #     self.customer_info_layout.addWidget(self.salesperson_input, 4, 3)

    #     self.upper_section_layout.addLayout(customer_info_layout)
    #     main_layout.addWidget(self.upper_section)

    #     # Middle section (Product table)
    #     self.product_table = QTableWidget()
    #     self.product_table.setColumnCount(6)
    #     self.product_table.setHorizontalHeaderLabels(["產品編號", "品名規格", "數量", "單位", "單價", "小計"])
    #     main_layout.addWidget(self.product_table)

    #     # Lower section (Total section + Additional info)
    #     self.lower_section = QWidget()
    #     self.lower_section.setStyleSheet("background-color: #f0f0f0;")
    #     self.lower_section.setGeometry(QRect(0, 0, 800, 200))  # Example size, adjust as needed

    #     lower_layout = QVBoxLayout(self.lower_section)
    #     lower_layout.setContentsMargins(10, 10, 10, 10)

    #     # Total section
    #     total_info_layout = QGridLayout()
    #     total_info_layout.setContentsMargins(0, 0, 0, 0)

    #     total_info_layout.addWidget(QLabel("折讓:"), 0, 0)
    #     self.discount_input = QLineEdit()
    #     self.discount_input.setFixedWidth(150)
    #     total_info_layout.addWidget(self.discount_input, 0, 1)
        
    #     total_info_layout.addWidget(QLabel("合計:"), 0, 2)
    #     self.total_input = QLineEdit()
    #     self.total_input.setFixedWidth(150)
    #     total_info_layout.addWidget(self.total_input, 0, 3)
        
    #     total_info_layout.addWidget(QLabel("備註:"), 1, 0)
    #     self.notes_input = QLineEdit()
    #     self.notes_input.setFixedWidth(150)
    #     total_info_layout.addWidget(self.notes_input, 1, 1)
        
    #     total_info_layout.addWidget(QLabel("已收:"), 1, 2)
    #     self.amount_received_input = QLineEdit()
    #     self.amount_received_input.setFixedWidth(150)
    #     total_info_layout.addWidget(self.amount_received_input, 1, 3)
        
    #     total_info_layout.addWidget(QLabel("稅額:"), 2, 0)
    #     self.tax_amount_input = QLineEdit()
    #     self.tax_amount_input.setFixedWidth(150)
    #     total_info_layout.addWidget(self.tax_amount_input, 2, 1)
        
    #     total_info_layout.addWidget(QLabel("未收:"), 2, 2)
    #     self.amount_due_input = QLineEdit()
    #     self.amount_due_input.setFixedWidth(150)
    #     total_info_layout.addWidget(self.amount_due_input, 2, 3)
        
    #     total_info_layout.addWidget(QLabel("總計:"), 3, 0)
    #     self.total_amount_input = QLineEdit()
    #     self.total_amount_input.setFixedWidth(150)
    #     total_info_layout.addWidget(self.total_amount_input, 3, 1)

    #     lower_layout.addLayout(total_info_layout)

    #     # Additional info
    #     additional_info_layout = QGridLayout()
    #     additional_info_layout.setContentsMargins(0, 0, 0, 0)

    #     additional_info_layout.addWidget(QLabel("主管:"), 0, 0)
    #     self.supervisor_input = QLineEdit()
    #     self.supervisor_input.setFixedWidth(150)
    #     additional_info_layout.addWidget(self.supervisor_input, 0, 1)
        
    #     additional_info_layout.addWidget(QLabel("會計:"), 0, 2)
    #     self.accountant_input = QLineEdit()
    #     self.accountant_input.setFixedWidth(150)
    #     additional_info_layout.addWidget(self.accountant_input, 0, 3)
        
    #     additional_info_layout.addWidget(QLabel("出納:"), 1, 0)
    #     self.cashier_input = QLineEdit()
    #     self.cashier_input.setFixedWidth(150)
    #     additional_info_layout.addWidget(self.cashier_input, 1, 1)
        
    #     additional_info_layout.addWidget(QLabel("客戶:"), 1, 2)
    #     self.customer_final_input = QLineEdit()
    #     self.customer_final_input.setFixedWidth(150)
    #     additional_info_layout.addWidget(self.customer_final_input, 1, 3)
        
    #     additional_info_layout.addWidget(QLabel("頁:"), 2, 0)
    #     self.page_number_input = QLineEdit("1/1")
    #     self.page_number_input.setFixedWidth(150)
    #     additional_info_layout.addWidget(self.page_number_input, 2, 1)

    #     lower_layout.addLayout(additional_info_layout)

    #     # Print button
    #     print_button = QPushButton("打印出貨單")
    #     print_button.clicked.connect(self.print_sales_receipt)
    #     lower_layout.addWidget(print_button)

    #     main_layout.addWidget(self.lower_section)


    # def print_sales_receipt(self):
    #     from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
    #     from PyQt6.QtGui import QPainter

    #     printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    #     printer.setPaperSize(QPrinter.PaperSize.A4)  # Use setPaperSize with QPrinter.PaperSize.A4
    #     printer.setOrientation(QPrinter.Orientation.Portrait)
        
    #     dialog = QPrintDialog(printer, self)
    #     if dialog.exec() == QPrintDialog.DialogCode.Accepted:
    #         painter = QPainter(printer)
    #         self.render(painter)  # Render the widget content to the printer
    #         painter.end()


