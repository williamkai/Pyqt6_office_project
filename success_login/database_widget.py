from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QWidget, 
                             QVBoxLayout, 
                             QHBoxLayout, 
                             QPushButton, 
                             QLabel,
                             QLineEdit,
                             QGridLayout, 
                             QTableWidget, 
                             QTableWidgetItem, 
                             QApplication,
                             QMessageBox,
                             QDialog,
                             QFormLayout
                             )

class DatabaseWidget(QWidget):

    closed = pyqtSignal()

    def __init__(self, parent=None, database=None):
        super().__init__(parent)
        self.database = database
        self.setWindowTitle("庫存資料庫功能")
        self.setMinimumSize(700, 600)
        
        self.main_layout = QVBoxLayout(self)
        
        # 上排的水平排列按鈕
        self.button_layout = QHBoxLayout()
        
        self.product_table_button = QPushButton("商品清單")
        self.product_table_button.clicked.connect(self.product_table)
        self.button_layout.addWidget(self.product_table_button)
        
        self.inventory_button = QPushButton("庫存功能")
        self.inventory_button.clicked.connect(self.inventory_function)
        self.button_layout.addWidget(self.inventory_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        # 顯示區域，使用QWidget
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        self.main_layout.addWidget(self.display_area)
        # 初始化GridLayout对象
        self.grid_layout = None
        self.table_widget = None

    def product_table(self):
        self.clear_display_area()
        self.database.create_product_list_table()
        
        # 从数据库中读取商品数据
        products = self.database.get_product_list()

        # 创建QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(products))
        self.table_widget.setColumnCount(8)  # 包括售价、修改和删除按钮在内的总列数
        self.table_widget.setHorizontalHeaderLabels(["商品代號", "商品名稱", "包數", "抽數", "廠商名稱", "售價", "修改", "刪除"])

        # 将数据填充到QTableWidget中
        for row_idx, row_data in enumerate(products):
            for col_idx, col_data in enumerate(row_data):
                if col_data is None:
                    col_data = ""  # 处理空值，显示为空字符串
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            
            modify_button = QPushButton("修改")
            modify_button.clicked.connect(lambda _, r=row_idx: self.modify_product(r))
            self.table_widget.setCellWidget(row_idx, 6, modify_button)

            delete_button = QPushButton("刪除")
            delete_button.clicked.connect(lambda _, r=row_idx: self.delete_product_confirmation(r))
            self.table_widget.setCellWidget(row_idx, 7, delete_button)

        # 如果表格为空，显示表头
        if not products:
            self.table_widget.setRowCount(1)
            for col_idx in range(8):  # 包括售价、修改和删除按钮在内的总列数
                self.table_widget.setItem(0, col_idx, QTableWidgetItem(""))

        self.display_layout.addWidget(self.table_widget)

        # 调整列宽
        self.table_widget.resizeColumnsToContents()
        
        # 在表格下面添加“新增商品”按钮
        add_product_button = QPushButton("新增商品")
        add_product_button.clicked.connect(self.add_product)
        self.display_layout.addWidget(add_product_button)

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
            product_id = int(self.table_widget.item(row, 0).text())
            self.database.delete_product(product_id)
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

    def inventory_function(self):
        self.clear_display_area()
        self.database.create_inventory_table()
        
        # 在顯示區域內加入庫存功能相關的小部件
        label = QLabel("庫存功能正在開發中...")
        self.display_layout.addWidget(label)

    def clear_display_area(self):
        # 清空顯示區域
        for i in reversed(range(self.display_layout.count())):
            widget = self.display_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # 清空GridLayout对象及其中的部件
        if self.grid_layout:
            while self.grid_layout.count():
                item = self.grid_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

            # 將布局管理器置空，以便重新使用
            self.grid_layout = None

    def submit_product(self, product_name):
        # 提交商品名稱等資料的處理
        self.clear_display_area()
        label = QLabel(f"已提交商品名稱: {product_name}")
        self.display_layout.addWidget(label)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()