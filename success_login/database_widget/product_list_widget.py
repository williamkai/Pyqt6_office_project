# product_list_widget.py
from PyQt6.QtWidgets import (QWidget, 
                             QVBoxLayout, 
                             QHBoxLayout, 
                             QPushButton, 
                             QLineEdit, 
                             QTableWidget, 
                             QTableWidgetItem, 
                             QMessageBox, QDialog, 
                             QFormLayout,
                             QDateTimeEdit, 
                             QCompleter, 
                             QComboBox)
from PyQt6.QtCore import QDateTime,Qt
# from data_access_object.product_list_dao import ProductListDao
class ProductListWidget(QWidget):

    def __init__(self, parent=None, database=None):
        super().__init__(parent)
        self.database = database
        self.initialize_ui() 
    
    def initialize_ui(self):
        self.layout = QVBoxLayout(self)
        self.product_table()
        
    def product_table(self):
        self.clear_layout()
        self.all_product_codes = self.database.inventory_dao.get_all_product_codes()
        products = self.database.product_list_dao.get_product_list()

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(products))
        self.table_widget.setColumnCount(10)
        self.table_widget.setHorizontalHeaderLabels(["商品代號", "商品名稱", "包數", "抽數", "廠商名稱", "售價", "庫存量", "修改", "刪除", "庫存功能"])

        for row_idx, row_data in enumerate(products):
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            
             # 查詢並顯示庫存量
            product_code = row_data[0]  # 假設商品代號在第一列
            inventory_amount = self.database.inventory_dao.get_latest_inventory(product_code)
            inventory_amount = inventory_amount if inventory_amount is not None else "無紀錄"
            self.table_widget.setItem(row_idx, 6, QTableWidgetItem(str(inventory_amount)))

            modify_button = QPushButton("修改")
            modify_button.clicked.connect(lambda _, r=row_idx: self.modify_product(r))
            self.table_widget.setCellWidget(row_idx, 7, modify_button)

            delete_button = QPushButton("刪除")
            delete_button.clicked.connect(lambda _, r=row_idx: self.delete_product_confirmation(r))
            self.table_widget.setCellWidget(row_idx, 8, delete_button)

            inventory_button = QPushButton("庫存功能")
            inventory_button.clicked.connect(lambda _, r=row_idx: self.add_inventory(r))
            self.table_widget.setCellWidget(row_idx, 9, inventory_button)  # 添加到第9列

        if not products:
            self.table_widget.setRowCount(1)
            for col_idx in range(10):
                self.table_widget.setItem(0, col_idx, QTableWidgetItem(""))

        self.layout.addWidget(self.table_widget)
        self.table_widget.resizeColumnsToContents()

        add_product_button = QPushButton("新增商品")
        add_product_button.clicked.connect(self.add_product)
        self.layout.addWidget(add_product_button)
    
    def modify_product(self, row):
        product_code = self.table_widget.item(row, 0).text()
        product_name = self.table_widget.item(row, 1).text()
        package_count = int(self.table_widget.item(row, 2).text())
        draw_count = int(self.table_widget.item(row, 3).text())
        manufacturer = self.table_widget.item(row, 4).text()
        price = float(self.table_widget.item(row, 5).text()) if self.table_widget.item(row, 5).text() else None

        dialog = QDialog(self)
        dialog.setWindowTitle("修改商品")
        layout = QFormLayout(dialog)

        product_name_edit = QLineEdit(product_name)
        package_count_edit = QLineEdit(str(package_count))
        draw_count_edit = QLineEdit(str(draw_count))
        manufacturer_edit = QLineEdit(manufacturer)
        price_edit = QLineEdit(str(price) if price is not None else "")

        layout.addRow("商品名稱", product_name_edit)
        layout.addRow("包數", package_count_edit)
        layout.addRow("抽數", draw_count_edit)
        layout.addRow("廠商名稱", manufacturer_edit)
        layout.addRow("售價", price_edit)

        buttons = QHBoxLayout()
        save_button = QPushButton("保存")
        save_button.clicked.connect(lambda: self.save_product(dialog, product_code, product_name_edit.text(), int(package_count_edit.text()), int(draw_count_edit.text()), manufacturer_edit.text(), float(price_edit.text()) if price_edit.text() else None))
        buttons.addWidget(save_button)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

        dialog.setLayout(layout)
        dialog.exec()

    def add_product(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("新增商品")
        layout = QFormLayout(dialog)

        product_code_edit = QLineEdit()
        product_name_edit = QLineEdit()
        package_count_edit = QLineEdit()
        draw_count_edit = QLineEdit()
        manufacturer_edit = QLineEdit()
        price_edit = QLineEdit()

        layout.addRow("商品代號", product_code_edit)
        layout.addRow("商品名稱", product_name_edit)
        layout.addRow("包數", package_count_edit)
        layout.addRow("抽數", draw_count_edit)
        layout.addRow("廠商名稱", manufacturer_edit)
        layout.addRow("售價", price_edit)

        buttons = QHBoxLayout()
        add_button = QPushButton("新增")
        add_button.clicked.connect(lambda: self.save_new_product(dialog, product_code_edit.text(), product_name_edit.text(), int(package_count_edit.text()), int(draw_count_edit.text()), manufacturer_edit.text(), float(price_edit.text()) if price_edit.text() else None))
        buttons.addWidget(add_button)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

        dialog.setLayout(layout)
        dialog.exec()

    def delete_product_confirmation(self, row):
        reply = QMessageBox.question(self, '刪除商品', '確定要刪除此商品嗎？',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            product_code =  self.table_widget.item(row, 0).text() 
            self.database.delete_product(product_code)
            QMessageBox.information(self, "信息", "商品已刪除")
            self.product_table()

    def save_new_product(self, dialog, product_code, product_name, package_count, draw_count, manufacturer, price):
        self.database.product_list_dao.insert_product(product_code, product_name, package_count, draw_count, manufacturer, price)
        QMessageBox.information(self, "信息", "商品已新增")
        dialog.accept()
        self.product_table()

    def save_product(self, dialog, product_code, product_name, package_count, draw_count, manufacturer, price):
        self.database.product_list_dao.update_product(product_code, product_name, package_count, draw_count, manufacturer, price)
        QMessageBox.information(self, "信息", "商品已更新")
        dialog.accept()
        self.product_table()

    def add_inventory(self, row_idx):
        dialog = QDialog(self)
        dialog.setWindowTitle("新增庫存變動")
        layout = QFormLayout(dialog)

        # 商品代號輸入框，帶有自動補全功能
        product_code_edit = QComboBox()
        product_code_edit.setEditable(True)
        product_code_edit.addItems(self.all_product_codes)
        # product_code_edit.setCompleter(QCompleter(self.all_product_codes))
        # 設定 QCompleter 並設定大小寫不敏感
        completer = QCompleter(self.all_product_codes)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        product_code_edit.setCompleter(completer)

        # 預填充商品代號
        item = self.table_widget.item(row_idx, 0)
        if item:
            product_code_edit.setCurrentText(item.text())

        # 日期時間輸入框，預設為當前日期和時間
        datetime_edit = QDateTimeEdit(calendarPopup=True)
        datetime_edit.setDateTime(QDateTime.currentDateTime())
        datetime_edit.setDisplayFormat('yyyy-MM-dd HH:mm')
        
        # 狀態選擇框
        status_edit = QComboBox()
        status_edit.addItems(["製造", "銷貨", "退貨", "瑕疵品"])

        quantity_edit = QLineEdit()

        # 備註輸入框
        notes_edit = QLineEdit()

        layout.addRow("商品代號", product_code_edit)
        layout.addRow("日期時間 (YYYY-MM-DD HH:MM)", datetime_edit)
        layout.addRow("狀態", status_edit)
        layout.addRow("數量", quantity_edit)
        layout.addRow("備註", notes_edit)  # 添加備註輸入框

        buttons = QHBoxLayout()
        add_button = QPushButton("新增")
        add_button.clicked.connect(lambda: self.save_inventory(
            dialog,
            None,
            product_code_edit.currentText(),  # 使用 currentText() 而不是 text()
            datetime_edit.dateTime().toString('yyyy-MM-dd HH:mm:ss'),
            status_edit.currentText(),  # 使用 currentText() 而不是 text()
            int(quantity_edit.text()),
            None,
            notes_edit.text()  # 傳遞備註的值,
        ))
        buttons.addWidget(add_button)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

        dialog.setLayout(layout)

        # 設定對話框大小
        dialog.resize(400, 150)  # 設定合適的寬度和高度

        dialog.exec()

    def save_inventory(self, dialog, inventory_id, product_code, date, status, quantity, current_stock, notes):
        if inventory_id is None:
            # 如果 inventory_id 为 None，则执行新增操作
            print("走這邊嗎????? 這便是新增商品庫存")
            self.database.inventory_dao.insert_inventory(product_code, date, status, quantity, notes)
            QMessageBox.information(self, "資訊", "庫存變動已新增")
        else:
            # 否则执行更新操作
            print("還是這邊??? 這邊是更新原有資料")
            self.database.inventory_dao.adjust_inventory_after_date(inventory_id, product_code, date, status, quantity, current_stock, notes)
            QMessageBox.information(self, "資訊", "庫存變動已更新")

        # 刷新商品表格，更新顯示的庫存量
        self.product_table()        
        dialog.accept()

    def clear_layout(self):
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
