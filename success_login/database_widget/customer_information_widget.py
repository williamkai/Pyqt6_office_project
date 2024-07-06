# customer_information_widget.py
'''
客戶資料建檔
痾痾痾痾，這邊處理到一半，發現需要把dao，重新設計，因為原本的方式會造成
成功登入後處理資料庫的程序越來越大包，所以要把本來的處理邏輯重新處理，
讓dao也把它做成物件導向的方式。
'''
from PyQt6.QtWidgets import (
                            QWidget, 
                            QVBoxLayout, 
                            QHBoxLayout, 
                            QPushButton, 
                            QLineEdit, 
                            QTableWidget, 
                            QTableWidgetItem,
                            QMessageBox, 
                            QDialog, 
                            QFormLayout, 
                            QDialogButtonBox,
                            QHeaderView
                        )

class CustomerInformation(QWidget):

    def __init__(self, parent=None, database=None):
        super().__init__(parent)
        self.database = database
        self.initialize_ui()

    def initialize_ui(self):
        self.layout = QVBoxLayout(self)
        self.customer_table()

    def customer_table(self):
        self.clear_layout()
        self.database.customer_dao.create_customer_information_table()
        
        customers = self.database.customer_dao.get_customer_list()

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(customers))
        self.table_widget.setColumnCount(13)  # Adjusted for email column
        self.table_widget.setHorizontalHeaderLabels(["",
            "客戶簡稱", "客戶名稱", "公司名稱", "發票台頭", "負責人", 
            "聯絡人", "電話", "行動電話", "公司地址", "電子郵件", "修改","刪除"
        ])
        self.table_widget.resizeColumnsToContents()
        self.table_widget.setColumnWidth(0, 0)  # 將第一列（庫存序列號列）的寬度設置為零，隱藏該列
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        for row_idx, row_data in enumerate(customers):
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            modify_button = QPushButton("修改")
            modify_button.clicked.connect(lambda _, r=row_idx: self.modify_customer(r))
            self.table_widget.setCellWidget(row_idx, 11, modify_button)

            delete_button = QPushButton("刪除")
            delete_button.clicked.connect(lambda _, r=row_idx: self.delete_customer_confirmation(r))
            self.table_widget.setCellWidget(row_idx, 12, delete_button)

        if not customers:
            self.table_widget.setRowCount(1)
            for col_idx in range(13):
                self.table_widget.setItem(0, col_idx, QTableWidgetItem(""))

        self.layout.addWidget(self.table_widget)
        self.table_widget.resizeColumnsToContents()

        add_customer_button = QPushButton("新增客戶")
        add_customer_button.clicked.connect(self.add_customer)
        self.layout.addWidget(add_customer_button)

    def modify_customer(self, row):
        customer_data = {
            'customer_id':self.table_widget.item(row, 0).text(),
            'short_name': self.table_widget.item(row, 1).text(),
            'full_name': self.table_widget.item(row, 2).text(),
            'company_name': self.table_widget.item(row, 3).text(),
            'invoice_title': self.table_widget.item(row, 4).text(),
            'manager': self.table_widget.item(row, 5).text(),
            'contact_person': self.table_widget.item(row, 6).text(),
            'phone': self.table_widget.item(row, 7).text(),
            'mobile': self.table_widget.item(row, 8).text(),
            'company_address': self.table_widget.item(row, 9).text(),
            'email': self.table_widget.item(row, 10).text(),
        }

        dialog = QDialog(self)
        dialog.setWindowTitle("修改客戶")
        layout = QFormLayout(dialog)

        short_name_edit = QLineEdit(customer_data['short_name'])
        full_name_edit = QLineEdit(customer_data['full_name'])
        company_name_edit = QLineEdit(customer_data['company_name'])
        invoice_title_edit = QLineEdit(customer_data['invoice_title'])
        manager_edit = QLineEdit(customer_data['manager'])
        contact_person_edit = QLineEdit(customer_data['contact_person'])
        phone_edit = QLineEdit(customer_data['phone'])
        mobile_edit = QLineEdit(customer_data['mobile'])
        company_address_edit = QLineEdit(customer_data['company_address'])
        email_edit = QLineEdit(customer_data['email'])

        layout.addRow("客戶簡稱", short_name_edit)
        layout.addRow("客戶名稱", full_name_edit)
        layout.addRow("公司名稱", company_name_edit)
        layout.addRow("發票台頭", invoice_title_edit)
        layout.addRow("負責人", manager_edit)
        layout.addRow("聯絡人", contact_person_edit)
        layout.addRow("電話", phone_edit)
        layout.addRow("行動電話", mobile_edit)
        layout.addRow("公司地址", company_address_edit)
        layout.addRow("電子郵件", email_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)

        def on_accept():
            self.database.customer_dao.update_customer(
                customer_data['id'], short_name_edit.text(), full_name_edit.text(), company_name_edit.text(),
                invoice_title_edit.text(), manager_edit.text(), contact_person_edit.text(),
                phone_edit.text(), mobile_edit.text(), company_address_edit.text(),
                 email_edit.text()
            )
            self.customer_table()
            dialog.accept()

        button_box.accepted.connect(on_accept)
        button_box.rejected.connect(dialog.reject)
        
        dialog.setLayout(layout)
        dialog.exec()

    def add_customer(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("新增客戶")
        layout = QFormLayout(dialog)

        short_name_edit = QLineEdit()
        full_name_edit = QLineEdit()
        company_name_edit = QLineEdit()
        invoice_title_edit = QLineEdit()
        manager_edit = QLineEdit()
        contact_person_edit = QLineEdit()
        phone_edit = QLineEdit()
        mobile_edit = QLineEdit()
        company_address_edit = QLineEdit()
        store_email_edit = QLineEdit()

        layout.addRow("客戶簡稱", short_name_edit)
        layout.addRow("客戶名稱", full_name_edit)
        layout.addRow("公司名稱", company_name_edit)
        layout.addRow("發票台頭", invoice_title_edit)
        layout.addRow("負責人", manager_edit)
        layout.addRow("聯絡人", contact_person_edit)
        layout.addRow("電話", phone_edit)
        layout.addRow("行動電話", mobile_edit)
        layout.addRow("公司地址", company_address_edit)
        layout.addRow("電子郵件", store_email_edit)

        buttons = QHBoxLayout()
        add_button = QPushButton("新增")
        add_button.clicked.connect(lambda: self.save_new_customer(dialog, 
                                                                  short_name_edit.text(), 
                                                                  full_name_edit.text(), 
                                                                  company_name_edit.text(), 
                                                                  invoice_title_edit.text(), 
                                                                  manager_edit.text(), 
                                                                  contact_person_edit.text(), 
                                                                  phone_edit.text(), 
                                                                  mobile_edit.text(), 
                                                                  company_address_edit.text(), 
                                                                  store_email_edit.text()))
        buttons.addWidget(add_button)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

        dialog.setLayout(layout)
        dialog.exec()

    def delete_customer_confirmation(self, row):
        reply = QMessageBox.question(self, '刪除客戶', '確定要刪除此客戶嗎？',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            customer_short_name = self.table_widget.item(row, 0).text()
            self.database.customer_dao.delete_customer(customer_short_name)
            QMessageBox.information(self, "信息", "客戶已刪除")
            self.customer_table()

    def save_new_customer(self, dialog, 
                          short_name, 
                          full_name, 
                          company_name, 
                          invoice_title, 
                          manager, 
                          contact_person, 
                          phone, 
                          mobile, 
                          company_address, 
                          store_email):
        self.database.customer_dao.insert_customer(short_name, 
                                                   full_name, 
                                                   company_name, 
                                                   invoice_title, 
                                                   manager, 
                                                   contact_person, 
                                                   phone, 
                                                   mobile, 
                                                   company_address, 
                                                   store_email)
        QMessageBox.information(self, "信息", "客戶已新增")
        dialog.accept()
        self.customer_table()

    def save_customer(self, dialog, row, short_name, full_name, company_name, invoice_title, manager, contact_person, phone, mobile, company_address, store_email):
        original_short_name = self.table_widget.item(row, 0).text()
        self.database.customer_dao.update_customer(original_short_name, short_name, full_name, company_name, invoice_title, manager, contact_person, phone, mobile, company_address, store_email)
        QMessageBox.information(self, "信息", "客戶已更新")
        dialog.accept()
        self.customer_table()

    def clear_layout(self):
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
