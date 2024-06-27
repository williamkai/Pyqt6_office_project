from PyQt6.QtCore import pyqtSignal,QDate,QDateTime
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
                             QFormLayout,
                             QComboBox,
                             QDateEdit,
                             QCompleter,
                             QDateTimeEdit,
                             QHeaderView,
                             )

class DatabaseWidget(QWidget):

    closed = pyqtSignal()

    def __init__(self, parent=None, database=None):
        super().__init__(parent)
        self.database = database
        self.setWindowTitle("庫存資料庫功能")
        self.setMinimumSize(900, 600)
        
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

    def inventory_function(self):
        self.clear_display_area()
        self.database.create_inventory_table()

        # 创建搜索框和按钮
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("請輸入商品代號")
        self.search_box.textChanged.connect(self.dynamic_search)  # 监听文本变化事件
        search_button = QPushButton("搜索")
        search_button.clicked.connect(self.search_inventory)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(search_button)

        self.display_layout.addLayout(search_layout)

        # 创建表格用于显示搜索结果
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(9)  # 包括“更改”和“删除”按钮
        self.table_widget.setHorizontalHeaderLabels(["", "商品代號", "日期", "狀態", "數量", "當前庫存量", "備註", "更改", "刪除"])
        # 將第一列的寬度設置為零，隱藏該列
        self.table_widget.setColumnWidth(0, 0)
        self.display_layout.addWidget(self.table_widget)

        # 初始化商品代号列表
        self.all_product_codes = self.database.get_all_product_codes()
        print(f"{self.all_product_codes}")

        # 添加新增庫存變動的按鈕
        add_inventory_button = QPushButton("新增庫存變動")
        add_inventory_button.clicked.connect(self.add_inventory)
        self.display_layout.addWidget(add_inventory_button)

    
    def add_inventory(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("新增庫存變動")
        layout = QFormLayout(dialog)

        # 商品代號輸入框，帶有自動補全功能
        product_code_edit = QComboBox()
        product_code_edit.setEditable(True)
        product_code_edit.addItems(self.all_product_codes)
        product_code_edit.setCompleter(QCompleter(self.all_product_codes))

        # 日期時間輸入框，默認為當前日期和時間
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

        # 設置對話框大小
        dialog.resize(400, 150)  # 設置合適的寬度和高度

        dialog.exec()

    def modify_inventory(self, row):
        inventory_id = self.table_widget.item(row, 0).text()
        product_code = self.table_widget.item(row, 1).text()
        date = self.table_widget.item(row, 2).text()
        status = self.table_widget.item(row, 3).text()
        quantity = int(self.table_widget.item(row, 4).text())
        current_stock = int(self.table_widget.item(row, 5).text())  # 获取当前库存量
        notes = self.table_widget.item(row, 6).text() if self.table_widget.item(row, 6) is not None else ''  # 获取备注信息

        dialog = QDialog(self)
        dialog.setWindowTitle("修改庫存")
        layout = QFormLayout(dialog)

        date_edit = QDateTimeEdit()
        date_edit.setDateTime(QDateTime.fromString(date, 'yyyy-MM-dd HH:mm:ss'))
        date_edit.setDisplayFormat('yyyy-MM-dd HH:mm')

        status_edit = QComboBox()
        status_edit.addItems(["製造", "銷貨", "退貨", "瑕疵品"])
        status_edit.setCurrentText(status)

        quantity_edit = QLineEdit(str(quantity))
        current_stock_label = QLabel(str(current_stock))  # 使用 QLabel 顯示當前庫存量，不可編輯

        notes_edit = QLineEdit(notes)  # 新增備註輸入框

        layout.addRow("日期時間 (YYYY-MM-DD HH:MM)", date_edit)
        layout.addRow("狀態", status_edit)
        layout.addRow("數量", quantity_edit)
        layout.addRow("當前庫存量", current_stock_label)  # 使用 QLabel 顯示當前庫存量
        layout.addRow("備註", notes_edit)  # 新增備註輸入框

        buttons = QHBoxLayout()
        save_button = QPushButton("保存")
        save_button.clicked.connect(lambda: self.save_inventory(
            dialog,
            inventory_id,
            product_code,
            date_edit.dateTime().toString('yyyy-MM-dd HH:mm:ss'),
            status_edit.currentText(),
            int(quantity_edit.text()),
            current_stock,
            notes_edit.text()  # 傳遞備註的值
        ))
        buttons.addWidget(save_button)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        buttons.addWidget(cancel_button)
        layout.addRow(buttons)

        dialog.setLayout(layout)

        # 設置對話框大小
        dialog.resize(400, 200)  # 設置合適的寬度和高度

        dialog.exec()


    def save_inventory(self, dialog, inventory_id, product_code, date, status, quantity, current_stock, notes):
        if inventory_id is None:
            # 如果 inventory_id 为 None，则执行新增操作
            print("走這邊嗎????? 這便是新增商品庫存")
            self.database.insert_inventory(product_code, date, status, quantity, notes)
            QMessageBox.information(self, "資訊", "庫存變動已新增")
        else:
            # 否则执行更新操作
            print("還是這邊??? 這邊是更新原有資料")
            self.database.adjust_inventory_after_date(inventory_id, product_code, date, status, quantity, current_stock, notes)
            QMessageBox.information(self, "資訊", "庫存變動已更新")

        dialog.accept()
        self.search_inventory()

    def delete_inventory_confirmation(self, row):
        reply = QMessageBox.question(self, '刪除庫存', '確定要刪除此庫存嗎？',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            inventory_id = self.table_widget.item(row, 0).text()
            self.database.delete_inventory(inventory_id)
            QMessageBox.information(self, "信息", "庫存已刪除")
            self.search_inventory()

    def dynamic_search(self):
        text = self.search_box.text().strip()
        if not text:
            return
        
        # 断开信号连接，避免多次调用
        self.search_box.textChanged.disconnect(self.dynamic_search)

        matches = []
        for code in self.all_product_codes:
            if text.upper() in code.upper():  # 不区分大小写进行匹配
                matches.append(code)

        if len(matches) == 1:
            self.search_box.setText(matches[0])  # 自动补全搜索框内容
            self.search_inventory()
        elif len(matches) == 0:
            QMessageBox.warning(self, "输入错误", "請輸入商品代號進行搜索")

        # 重新连接信号
        self.search_box.textChanged.connect(self.dynamic_search)

    def search_inventory(self):
        product_code = self.search_box.text()
        if not product_code:
            QMessageBox.warning(self, "输入错误", "請輸入商品代號進行搜索")
            return

        # 从数据库中获取库存数据
        inventory_data = self.database.search_inventory(product_code)

        if not inventory_data:
            QMessageBox.information(self, "無結果", "沒有找到該商品的庫存紀錄")
            return

        # 更新表格内容
        self.table_widget.setRowCount(len(inventory_data))
        for row_idx, row_data in enumerate(inventory_data):
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            current_stock_item = QTableWidgetItem(str(row_data[-2]))  # 获取倒数第二个元素作为当前库存量
            self.table_widget.setItem(row_idx, 5, current_stock_item)

            notes_item = QTableWidgetItem(row_data[-1])  # 获取最后一个元素作为备注
            self.table_widget.setItem(row_idx, 6, notes_item)

            modify_button = QPushButton("更改")
            modify_button.clicked.connect(lambda _, r=row_idx: self.modify_inventory(r))
            self.table_widget.setCellWidget(row_idx, 7, modify_button)

            delete_button = QPushButton("刪除")
            delete_button.clicked.connect(lambda _, r=row_idx: self.delete_inventory_confirmation(r))
            self.table_widget.setCellWidget(row_idx, 8, delete_button)

        # 调整列宽
        self.table_widget.resizeColumnsToContents()
        self.table_widget.setColumnWidth(0, 0)  # 將第一列（庫存序列號列）的寬度設置為零，隱藏該列
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)




    def clear_display_area(self):
        # 清空顯示區域
        while self.display_layout.count() > 0:
            item = self.display_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 清空GridLayout对象及其中的部件
        if self.grid_layout:
            while self.grid_layout.count() > 0:
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