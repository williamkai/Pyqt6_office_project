# product_list_widget.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
                             QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout,
                             QDateTimeEdit, QCompleter, QComboBox)
from PyQt6.QtCore import QDateTime, Qt, QDate, QTimer
from functools import partial


class ProductListWidget(QWidget):
    def __init__(self, parent=None, database=None):
        super().__init__(parent)
        self.database = database
        self.parent_widget = parent
        self.all_product_codes = None
        self.last_search_text = ""
        self.initialize_ui()

    def initialize_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.create_query_area()
        self.table_layout = QVBoxLayout()
        self.main_layout.addLayout(self.table_layout)
        self.product_table()

    def create_query_area(self):
        self.query_layout = QHBoxLayout()

        self.query_edit = QLineEdit()
        self.query_edit.setPlaceholderText("輸入商品代號查詢...")
        self.query_edit.textChanged.connect(self.dynamic_search)
        self.query_button = QPushButton("查詢")
        self.query_button.clicked.connect(self.perform_query)

        # 設定 completer
        self.all_product_codes = self.database.inventory_dao.get_all_product_codes()
        completer = QCompleter(self.all_product_codes)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.query_edit.setCompleter(completer)

        self.query_layout.addWidget(self.query_edit)
        self.query_layout.addWidget(self.query_button)

        self.main_layout.addLayout(self.query_layout)

        if isinstance(self.last_search_text, str) and self.last_search_text:
            self.query_edit.setText(self.last_search_text)
            self.dynamic_search()

    def perform_query(self):
        query_code = self.query_edit.text().strip()
        if query_code:
            self.update_product_table(query_code)
            completer = self.query_edit.completer()
            if completer:
                completer.popup().hide()
        else:
            QMessageBox.warning(self, "警告", "請輸入商品代號進行查詢")

    def product_table(self):
        self.update_product_table()

    def create_button(self, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        return button

    def add_buttons_to_row(self, row_idx, product_code):
        self.table_widget.setCellWidget(row_idx, 7, self.create_button("修改", partial(self.modify_product, row_idx)))
        self.table_widget.setCellWidget(row_idx, 8, self.create_button("刪除", partial(self.delete_product_confirmation, row_idx)))
        self.table_widget.setCellWidget(row_idx, 9, self.create_button("庫存功能", partial(self.add_inventory, row_idx)))

        if self.parent_widget and hasattr(self.parent_widget, 'show_inventory_function'):
            transfer_callback = partial(self.parent_widget.show_inventory_function, product_code)
        else:
            transfer_callback = partial(lambda r: print(f"Parent method not available, row {r}"), row_idx)

        self.table_widget.setCellWidget(row_idx, 10, self.create_button("轉庫存表", transfer_callback))

    def update_product_table(self, query_code=None):
        for i in reversed(range(self.table_layout.count())):
            widget = self.table_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        try:
            products = self.database.product_list_dao.get_product_list(query_code)
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"無法獲取產品列表: {str(e)}")
            return

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(products))
        self.table_widget.setColumnCount(11)
        self.table_widget.setHorizontalHeaderLabels([
            "商品代號", "商品名稱", "包數", "抽數", "廠商名稱", "售價", "庫存量", "修改",
            "刪除", "庫存功能", "轉庫存表"
        ])

        for row_idx, row_data in enumerate(products):
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            product_code = row_data[0]
            try:
                inventory_amount = self.database.inventory_dao.get_latest_inventory(product_code)
            except Exception as e:
                QMessageBox.critical(self, "錯誤", f"無法獲取庫存量: {str(e)}")
                inventory_amount = "無紀錄"

            self.table_widget.setItem(row_idx, 6, QTableWidgetItem(str(inventory_amount)))
            self.add_buttons_to_row(row_idx, product_code)

        if not products:
            self.table_widget.setRowCount(1)
            for col_idx in range(11):
                self.table_widget.setItem(0, col_idx, QTableWidgetItem(""))

        self.table_layout.addWidget(self.table_widget)
        self.table_widget.resizeColumnsToContents()

        add_product_button = self.create_button("新增商品", self.add_product)
        self.table_layout.addWidget(add_product_button)

    def dynamic_search(self):
        text = self.query_edit.text().strip()
        if len(text) > len(self.last_search_text):
            matches = [code for code in self.all_product_codes if text.upper() in code.upper()]
            if len(matches) == 1:
                self.query_edit.setText(matches[0])
                self.perform_query()
                self.last_search_text = matches[0]
                QTimer.singleShot(100, lambda: self.query_edit.completer().popup().hide())
        else:
            self.last_search_text = text

    def create_product_dialog(self, title, product=None):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QFormLayout(dialog)
        product_code_edit = QLineEdit()

        if product:
            product_code_edit.setText(product[0])
            product_code_edit.setReadOnly(True)  # Make product code read-only for editing
        else:
            product_code_edit.setPlaceholderText("輸入商品代號")

        product_name_edit = QLineEdit() if product is None else QLineEdit(product[1])
        package_count_edit = QLineEdit() if product is None else QLineEdit(str(product[2]))
        draw_count_edit = QLineEdit() if product is None else QLineEdit(str(product[3]))
        manufacturer_edit = QLineEdit() if product is None else QLineEdit(product[4])
        price_edit = QLineEdit() if product is None else QLineEdit(str(product[5]))

        # product_code_edit = QLineEdit() if product is None else QLineEdit(product[0])
        # product_name_edit = QLineEdit() if product is None else QLineEdit(product[1])
        # package_count_edit = QLineEdit() if product is None else QLineEdit(str(product[2]))
        # draw_count_edit = QLineEdit() if product is None else QLineEdit(str(product[3]))
        # manufacturer_edit = QLineEdit() if product is None else QLineEdit(product[4])
        # price_edit = QLineEdit() if product is None else QLineEdit(str(product[5]))

        layout.addRow("商品代號", product_code_edit)
        layout.addRow("商品名稱", product_name_edit)
        layout.addRow("包數", package_count_edit)
        layout.addRow("抽數", draw_count_edit)
        layout.addRow("廠商名稱", manufacturer_edit)
        layout.addRow("售價", price_edit)

        buttons = QHBoxLayout()
        # 根據是否是編輯模式，選擇相應的保存按鈕功能
        if product:
            save_button = self.create_button(
                "保存", 
                lambda: self.save_product(
                    dialog, 
                    product_code_edit.text().strip(), 
                    product_name_edit.text().strip(), 
                    package_count_edit.text().strip(), 
                    draw_count_edit.text().strip(), 
                    manufacturer_edit.text().strip(), 
                    price_edit.text().strip()
                )
            )
        else:
            save_button = self.create_button(
                "新增", 
                lambda: self.save_new_product(
                    dialog, 
                    product_code_edit.text().strip(), 
                    product_name_edit.text().strip(), 
                    package_count_edit.text().strip(), 
                    draw_count_edit.text().strip(), 
                    manufacturer_edit.text().strip(), 
                    price_edit.text().strip()
                )
            )
        buttons.addWidget(save_button)
        cancel_button = self.create_button("取消", dialog.reject)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

        dialog.setLayout(layout)
        dialog.exec()

    def modify_product(self, row):
        product = [self.table_widget.item(row, i).text() for i in range(6)]
        self.create_product_dialog("修改商品", product)

    def add_product(self):
        self.create_product_dialog("新增商品")

    def delete_product_confirmation(self, row):
        reply = QMessageBox.question(
            self, '刪除商品', '確定要刪除此商品嗎？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            product_code = self.table_widget.item(row, 0).text()
            try:
                self.database.product_list_dao.delete_product(product_code)
            except Exception as e:
                QMessageBox.critical(self, "錯誤", f"無法刪除商品: {str(e)}")
                return
            QMessageBox.information(self, "信息", "商品已刪除")
            self.product_table()

    def save_new_product(self, dialog, product_code, product_name, package_count, draw_count, manufacturer, price):
        try:
            self.database.product_list_dao.insert_product(
                product_code, product_name, package_count, draw_count, manufacturer, price
            )
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"無法新增商品: {str(e)}")
            return
        QMessageBox.information(self, "信息", "商品已新增")
        dialog.accept()
        self.product_table()

    def save_product(self, dialog, product_code, product_name, package_count, draw_count, manufacturer, price):
        try:
            self.database.product_list_dao.update_product(
                product_code, product_name, package_count, draw_count, manufacturer, price
            )
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"無法更新商品: {str(e)}")
            return
        QMessageBox.information(self, "信息", "商品已更新")
        dialog.accept()
        self.product_table()

    def add_inventory(self, row_idx):
        dialog = QDialog(self)
        dialog.setWindowTitle("新增庫存變動")
        layout = QFormLayout(dialog)

        product_code_edit = QComboBox()
        product_code_edit.setEditable(True)
        product_code_edit.addItems(self.all_product_codes)
        completer = QCompleter(self.all_product_codes)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        product_code_edit.setCompleter(completer)

        item = self.table_widget.item(row_idx, 0)
        if item:
            product_code_edit.setCurrentText(item.text())

        datetime_edit = QDateTimeEdit(calendarPopup=True)
        datetime_edit.setDateTime(QDateTime.currentDateTime())
        datetime_edit.setDisplayFormat('yyyy-MM-dd HH:mm')

        today_date = QDate.currentDate()
        today_date_str = today_date.toString('MM/dd')

        status_edit = QComboBox()
        status_edit.addItems(["製造", "銷貨", "退貨", "瑕疵品"])

        quantity_edit = QLineEdit()
        notes_edit = QLineEdit()
        notes_edit.setText(today_date_str)

        layout.addRow("商品代號", product_code_edit)
        layout.addRow("日期時間 (YYYY-MM-DD HH:MM)", datetime_edit)
        layout.addRow("狀態", status_edit)
        layout.addRow("數量", quantity_edit)
        layout.addRow("備註", notes_edit)

        buttons = QHBoxLayout()
        add_button = QPushButton("新增")
        add_button.clicked.connect(
        lambda: self.handle_save_inventory(
            dialog, product_code_edit.currentText(),
            datetime_edit.dateTime().toString('yyyy-MM-dd HH:mm:ss'),
            status_edit.currentText(), quantity_edit.text(),  # 這裡傳遞原始文本
            None, notes_edit.text()
        )
    )
        buttons.addWidget(add_button)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

        dialog.setLayout(layout)
        dialog.resize(400, 150)
        dialog.exec()

    def handle_save_inventory(self, dialog, product_code, date, status, quantity_text, current_stock, notes):
        try:
            quantity = int(quantity_text)  # 嘗試將文本轉換為整數
            if quantity < 0:
                raise ValueError("數量不能為負數")
        except ValueError:
            QMessageBox.warning(self, "錯誤", "請輸入有效的非負整數數量")
            return

        # 如果成功轉換數量，繼續調用 save_inventory
        self.save_inventory(dialog, None, product_code, date, status, quantity, current_stock, notes)
            
    def save_inventory(self, dialog, inventory_id, product_code, date, status, quantity, current_stock, notes):
        try:
            if inventory_id is None:
                self.database.inventory_dao.insert_inventory(
                    product_code, date, status, quantity, notes
                )
            else:
                self.database.inventory_dao.adjust_inventory_after_date(
                    inventory_id, product_code, date, status, quantity, current_stock, notes
                )
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"無法保存庫存變動: {str(e)}")
            return
        QMessageBox.information(self, "資訊", "庫存變動已新增")
        self.product_table()
        dialog.accept()
