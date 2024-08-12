# inventory_widget.py
from PyQt6.QtWidgets import (QWidget, 
                             QVBoxLayout, 
                             QHBoxLayout, 
                             QPushButton, 
                             QLineEdit, 
                             QTableWidget, 
                             QTableWidgetItem, 
                             QMessageBox, 
                             QDialog, 
                             QFormLayout, 
                             QComboBox, 
                             QDateTimeEdit, 
                             QCompleter,
                             QLabel,
                             QHeaderView
                             )
from PyQt6.QtCore import QDateTime,Qt,QDate

class InventoryWidget(QWidget):

    def __init__(self, parent=None, database=None,product_code=""):
        super().__init__(parent)
        self.database = database
        # 使用判斷式確保 self.last_search_text 是字符串
        if isinstance(product_code, str) and product_code:
            self.last_search_text = product_code
        else:
            self.last_search_text = ""
        
        print(f"{self.last_search_text}")
        print(f"{self.last_search_text}")
        self.initialize_ui()

    def initialize_ui(self):
        self.layout = QVBoxLayout(self)
        self.inventory_function()
        # self.last_search_text = ""

    def inventory_function(self):
        self.clear_layout()

        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("請輸入商品代號")
        self.search_box.textChanged.connect(self.dynamic_search)
        search_button = QPushButton("搜索")
        search_button.clicked.connect(self.search_inventory)

        search_layout.addWidget(self.search_box)
        search_layout.addWidget(search_button)
        self.layout.addLayout(search_layout)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(9)
        self.table_widget.setHorizontalHeaderLabels(["", "商品代號", "日期", "狀態", "數量", "當前庫存量", "備註", "更改", "刪除"])
        self.table_widget.setColumnWidth(0, 0)
        self.layout.addWidget(self.table_widget)

        self.all_product_codes = self.database.inventory_dao.get_all_product_codes()

        add_inventory_button = QPushButton("新增庫存變動")
        add_inventory_button.clicked.connect(self.add_inventory)
        self.layout.addWidget(add_inventory_button)
        # 確保 last_search_text 是字串
        if isinstance(self.last_search_text, str) and self.last_search_text:
            self.search_box.setText(self.last_search_text)
            self.search_inventory()
        else:
            # 處理 last_search_text 不是字串的情況
            self.search_box.setText("")




    def add_inventory(self):
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

        item = self.last_search_text
        if item:
            product_code_edit.setCurrentText(item)

        # 日期時間輸入框，默認為當前日期和時間
        datetime_edit = QDateTimeEdit(calendarPopup=True)
        datetime_edit.setDateTime(QDateTime.currentDateTime())
        datetime_edit.setDisplayFormat('yyyy-MM-dd HH:mm')
        # 預設填入今天的日期 (MM/dd) 到備註框
        today_date = QDate.currentDate()
        today_date_str = today_date.toString('MM/dd')

        # 狀態選擇框
        status_edit = QComboBox()
        status_edit.addItems(["製造", "銷貨", "退貨", "瑕疵品"])

        quantity_edit = QLineEdit()

        # 備註輸入框
        notes_edit = QLineEdit()
        notes_edit.setText(today_date_str)

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
            self.database.inventory_dao.insert_inventory(product_code, date, status, quantity, notes)
            QMessageBox.information(self, "資訊", "庫存變動已新增")
        else:
            # 否则执行更新操作
            print("還是這邊??? 這邊是更新原有資料")
            self.database.inventory_dao.adjust_inventory_after_date(inventory_id, product_code, date, status, quantity, current_stock, notes)
            QMessageBox.information(self, "資訊", "庫存變動已更新")

        dialog.accept()
        self.search_inventory()

    def delete_inventory_confirmation(self, row):
        reply = QMessageBox.question(self, '刪除庫存', '確定要刪除此庫存嗎？',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            inventory_id = self.table_widget.item(row, 0).text()
            inventory_code=self.table_widget.item(row, 1).text()
            self.database.inventory_dao.delete_inventory(inventory_id,inventory_code)
            QMessageBox.information(self, "信息", "庫存已刪除")
            self.search_inventory()

    def dynamic_search(self):
        text = self.search_box.text().strip()
        if not text:
            return
        
        # 断开信号连接，避免多次调用
        self.search_box.textChanged.disconnect(self.dynamic_search)
        print(f'text: {text}, type: {type(text)}')
        print(f'self.last_search_text: {self.last_search_text}, type: {type(self.last_search_text)}')

        # 判断是输入文字还是删除文字
        if len(text) > len(self.last_search_text):
            matches = []
            for code in self.all_product_codes:
                if text.upper() in code.upper():  # 不区分大小写进行匹配
                    matches.append(code)

            if len(matches) == 1:
                self.search_box.setText(matches[0])  # 自动补全搜索框内容
                self.last_search_text = matches[0] 
                self.search_inventory()
        else:
            # 如果是删除文字，什么都不做
            self.last_search_text = text
            pass

        # 重新连接信号
        self.search_box.textChanged.connect(self.dynamic_search)

    def search_inventory(self):
        product_code = self.search_box.text()
        if not product_code:
            QMessageBox.warning(self, "输入错误", "請輸入商品代號進行搜索")
            return

        # 从数据库中获取库存数据
        inventory_data = self.database.inventory_dao.search_inventory(product_code)
        print(inventory_data)

        if not inventory_data:
            QMessageBox.information(self, "無結果", "沒有找到該商品的庫存紀錄")
            return

        # 更新表格内容
        self.table_widget.setRowCount(len(inventory_data))
        for row_idx, row_data in enumerate(inventory_data):
            print(f"Row {row_idx}: {row_data}")  # 列印每行數據，確認順序
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


    def clear_layout(self):
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
