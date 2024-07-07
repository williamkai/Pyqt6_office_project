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
                            QHeaderView,
                            QLabel
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
        self.table_widget.setColumnCount(8)  # 調整為顯示的列數
        self.table_widget.setHorizontalHeaderLabels([
            "客戶簡稱", "公司名稱", "聯絡人", "電話", 
            "行動電話", "公司地址", "修改", "刪除"
        ])
        self.table_widget.resizeColumnsToContents()

        for row_idx, row_data in enumerate(customers):
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            modify_button = QPushButton("修改")
            modify_button.clicked.connect(lambda _, r=row_idx: self.modify_customer(r))
            self.table_widget.setCellWidget(row_idx, 6, modify_button)

            delete_button = QPushButton("刪除")
            delete_button.clicked.connect(lambda _, r=row_idx: self.delete_customer_confirmation(r))
            self.table_widget.setCellWidget(row_idx, 7, delete_button)

        if not customers:
            self.table_widget.setRowCount(1)
            for col_idx in range(8):
                self.table_widget.setItem(0, col_idx, QTableWidgetItem(""))

        self.layout.addWidget(self.table_widget)
        self.table_widget.resizeColumnsToContents()

        add_customer_button = QPushButton("新增客戶")
        add_customer_button.clicked.connect(self.add_customer)
        self.layout.addWidget(add_customer_button)

    def modify_customer(self, row):
        company_name = self.table_widget.item(row, 1).text()  # 客戶ID在第二個欄位（索引為1）

        customer_data = self.database.customer_dao.get_customer_company_name(company_name)

        if customer_data:
            dialog = QDialog(self)
            dialog.setWindowTitle("修改客戶")
            layout = QFormLayout(dialog)

            short_name_edit = QLineEdit(customer_data['short_name'])
            company_name_edit = QLineEdit(customer_data['company_name'])
            # vat_number_edit = QLineEdit(customer_data['vat_number'])
            manager_edit = QLineEdit(customer_data['manager'])
            contact_person_edit = QLineEdit(customer_data['contact_person'])
            phone_edit = QLineEdit(customer_data['phone'])
            mobile_edit = QLineEdit(customer_data['mobile'])
            company_address_edit = QLineEdit(customer_data['company_address'])
            email_edit = QLineEdit(customer_data['email'])
            vat_number_edit = QLineEdit(customer_data['vat_number'])
            phone2_edit = QLineEdit(customer_data['phone2'])
            fax_edit = QLineEdit(customer_data['fax'])
            factory_address_edit = QLineEdit(customer_data['factory_address'])
            website_edit = QLineEdit(customer_data['website'])
            line_id_edit = QLineEdit(customer_data['line_id'])
            notes_edit = QLineEdit(customer_data['notes'])

            # 客戶ID設為不可編輯
            customer_id_label = QLabel(customer_data['id'])

            layout.addRow("客戶ID", customer_id_label)
            layout.addRow("客戶簡稱", short_name_edit)
            layout.addRow("公司名稱", company_name_edit)
            layout.addRow("統一編號", vat_number_edit)
            layout.addRow("負責人", manager_edit)
            layout.addRow("聯絡人", contact_person_edit)
            layout.addRow("電話1", phone_edit)
            layout.addRow("電話2", phone2_edit)
            layout.addRow("傳真", fax_edit)
            layout.addRow("行動電話", mobile_edit)
            layout.addRow("電子郵件", email_edit)
            layout.addRow("公司地址", company_address_edit)
            layout.addRow("工廠地址", factory_address_edit)
            layout.addRow("網址", website_edit)
            layout.addRow("LINE ID", line_id_edit)
            layout.addRow("備註", notes_edit)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            layout.addWidget(button_box)

            def on_accept():
                update_success = self.database.customer_dao.update_customer(
                    customer_data['id'], short_name_edit.text(), company_name_edit.text(),
                    vat_number_edit.text(), manager_edit.text(), contact_person_edit.text(),
                    phone_edit.text(), phone2_edit.text(), fax_edit.text(), mobile_edit.text(),
                    email_edit.text(), company_address_edit.text(), factory_address_edit.text(),
                    website_edit.text(), line_id_edit.text(), notes_edit.text()
                )

                if update_success:
                    self.customer_table()
                    dialog.accept()
                else:
                    QMessageBox.warning(self, "錯誤", "公司名稱已存在或更新失敗。")

            button_box.accepted.connect(on_accept)
            button_box.rejected.connect(dialog.reject)
            
            dialog.setLayout(layout)
            dialog.exec()
        else:
            QMessageBox.warning(self, "錯誤", "找不到該客戶的資料。")

    def add_customer(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("新增客戶")
        layout = QFormLayout(dialog)

        short_name_edit = QLineEdit()
        company_name_edit = QLineEdit()
        vat_number_edit = QLineEdit()
        manager_edit = QLineEdit()
        contact_person_edit = QLineEdit()
        phone_edit = QLineEdit()
        phone2_edit = QLineEdit()
        fax_edit = QLineEdit()
        mobile_edit = QLineEdit()
        email_edit = QLineEdit()
        company_address_edit = QLineEdit()
        factory_address_edit = QLineEdit()
        website_edit = QLineEdit()
        line_id_edit = QLineEdit()
        notes_edit = QLineEdit()

        layout.addRow("客戶簡稱", short_name_edit)
        layout.addRow("公司名稱", company_name_edit)
        layout.addRow("統一發票", vat_number_edit)
        layout.addRow("負責人", manager_edit)
        layout.addRow("聯絡人", contact_person_edit)
        layout.addRow("電話1", phone_edit)
        layout.addRow("電話2", phone2_edit)
        layout.addRow("傳真", fax_edit)
        layout.addRow("行動電話", mobile_edit)
        layout.addRow("電子郵件", email_edit)
        layout.addRow("公司地址", company_address_edit)
        layout.addRow("工廠地址", factory_address_edit)
        layout.addRow("網址", website_edit)
        layout.addRow("LINE ID", line_id_edit)
        layout.addRow("備註", notes_edit)

        buttons = QHBoxLayout()
        add_button = QPushButton("新增")
        add_button.clicked.connect(lambda: self.save_new_customer(dialog,
                                                                short_name_edit.text(),
                                                                company_name_edit.text(),
                                                                vat_number_edit.text(),
                                                                manager_edit.text(),
                                                                contact_person_edit.text(),
                                                                phone_edit.text(),
                                                                phone2_edit.text(),
                                                                fax_edit.text(),
                                                                mobile_edit.text(),
                                                                email_edit.text(),
                                                                company_address_edit.text(),
                                                                factory_address_edit.text(),
                                                                website_edit.text(),
                                                                line_id_edit.text(),
                                                                notes_edit.text()))
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

    def save_new_customer(
            self, dialog,short_name,company_name,vat_number, 
            manager,contact_person,phone1,phone2,fax,mobile,email,company_address, 
            factory_address,website, line_id,notes):
        # Perform validation or any necessary checks here before inserting

        # Example: Check if company name already exists
        if self.database.customer_dao.check_company_name_exist(company_name):
            QMessageBox.warning(self, "錯誤", "公司名稱已存在，請使用不同的公司名稱。")
            return

        # Insert customer data into the database
        self.database.customer_dao.insert_customer(
                short_name,company_name,vat_number,manager, 
                contact_person, phone1, phone2,fax,mobile,email,company_address, 
                factory_address,website,line_id,notes)
        
        QMessageBox.information(self, "資訊", "客戶已新增")
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
