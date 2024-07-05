# product_list_widget.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QComboBox)

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
        self.database.create_product_list_table()
        
        products = self.database.get_product_list()

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(products))
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(["商品代號", "商品名稱", "包數", "抽數", "廠商名稱", "售價", "修改", "刪除"])

        for row_idx, row_data in enumerate(products):
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            
            modify_button = QPushButton("修改")
            modify_button.clicked.connect(lambda _, r=row_idx: self.modify_product(r))
            self.table_widget.setCellWidget(row_idx, 6, modify_button)

            delete_button = QPushButton("刪除")
            delete_button.clicked.connect(lambda _, r=row_idx: self.delete_product_confirmation(r))
            self.table_widget.setCellWidget(row_idx, 7, delete_button)

        if not products:
            self.table_widget.setRowCount(1)
            for col_idx in range(8):
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
        self.database.insert_product(product_code, product_name, package_count, draw_count, manufacturer, price)
        QMessageBox.information(self, "信息", "商品已新增")
        dialog.accept()
        self.product_table()

    def save_product(self, dialog, product_code, product_name, package_count, draw_count, manufacturer, price):
        self.database.update_product(product_code, product_name, package_count, draw_count, manufacturer, price)
        QMessageBox.information(self, "信息", "商品已更新")
        dialog.accept()
        self.product_table()

    def clear_layout(self):
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
