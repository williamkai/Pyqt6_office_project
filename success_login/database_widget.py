from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QWidget, 
                             QVBoxLayout, 
                             QHBoxLayout, 
                             QPushButton, 
                             QLabel,
                             QLineEdit,
                             QGridLayout
                             )

class DatabaseWidget(QWidget):

    closed = pyqtSignal()

    def __init__(self, parent=None, database=None):
        super().__init__(parent)
        self.database = database
        self.setWindowTitle("庫存資料庫功能")
        self.setMinimumSize(800, 600)
        
        self.main_layout = QVBoxLayout(self)
        
        # 上排的水平排列按鈕
        self.button_layout = QHBoxLayout()
        
        self.create_product_button = QPushButton("建立商品基本資料")
        self.create_product_button.clicked.connect(self.create_product)
        self.button_layout.addWidget(self.create_product_button)
        
        self.inventory_button = QPushButton("庫存功能")
        self.inventory_button.clicked.connect(self.inventory_function)
        self.button_layout.addWidget(self.inventory_button)
        
        self.product_table_button = QPushButton("商品總表")
        self.product_table_button.clicked.connect(self.product_table)
        self.button_layout.addWidget(self.product_table_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        # 顯示區域，使用QWidget
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        self.main_layout.addWidget(self.display_area)
        # 初始化GridLayout对象
        self.grid_layout = None

    def create_product(self):
        self.clear_display_area()
        self.database.create_product_list_table()

        # 使用QGridLayout进行布局
        grid_layout = QGridLayout()

        label_product_name = QLabel("商品名稱:")
        grid_layout.addWidget(label_product_name, 0, 0, 1, 1)

        line_edit_product_name = QLineEdit()
        line_edit_product_name.setFixedWidth(200)
        grid_layout.addWidget(line_edit_product_name, 0, 1, 1, 4)

        label_product_code = QLabel("商品代號:")
        grid_layout.addWidget(label_product_code, 1, 0, 1, 1)

        line_edit_product_code = QLineEdit()
        line_edit_product_code.setFixedWidth(200)
        grid_layout.addWidget(line_edit_product_code, 1, 1, 1, 4)

        label_package_count = QLabel("包數:")
        grid_layout.addWidget(label_package_count, 2, 0, 1, 1)

        line_edit_package_count = QLineEdit()
        line_edit_package_count.setFixedWidth(200)
        grid_layout.addWidget(line_edit_package_count, 2, 1, 1, 4)

        label_draw_count = QLabel("抽數:")
        grid_layout.addWidget(label_draw_count, 3, 0, 1, 1)

        line_edit_draw_count = QLineEdit()
        line_edit_draw_count.setFixedWidth(200)
        grid_layout.addWidget(line_edit_draw_count, 3, 1, 1, 4)

        label_manufacturer = QLabel("廠商名稱:")
        grid_layout.addWidget(label_manufacturer, 4, 0, 1, 1)

        line_edit_manufacturer = QLineEdit()
        line_edit_manufacturer.setFixedWidth(200)
        grid_layout.addWidget(line_edit_manufacturer, 4, 1, 1, 4)

        label_price = QLabel("售價:")
        grid_layout.addWidget(label_price, 5, 0, 1, 1)

        line_edit_price = QLineEdit()
        line_edit_price.setFixedWidth(200)
        grid_layout.addWidget(line_edit_price, 5, 1, 1, 4)

        submit_button = QPushButton("提交")
        submit_button.setFixedSize(200, 40)
        submit_button.clicked.connect(lambda: self.submit_product(line_edit_product_code.text(),
                                                                  line_edit_product_name.text(),
                                                                  int(line_edit_package_count.text()),
                                                                  int(line_edit_draw_count.text()),
                                                                  line_edit_manufacturer.text(),
                                                                  float(line_edit_price.text()) if line_edit_price.text() else None))
        grid_layout.addWidget(submit_button, 6, 2, 1, 1)  # 将提交按钮放在第7行第3列，占据1行1列

        # 设置列的伸展因子，让中间的列（第2列）伸展以填充空白空间，从而将提交按钮置中
        grid_layout.setColumnStretch(1, 1)

        self.display_layout.addLayout(grid_layout)


    def inventory_function(self):
        self.clear_display_area()
        
        # 在顯示區域內加入庫存功能相關的小部件
        label = QLabel("庫存功能正在開發中...")
        self.display_layout.addWidget(label)

    def product_table(self):
        self.clear_display_area()
        
        # 在顯示區域內顯示商品總表資料
        label = QLabel("商品總表資料顯示區域...")
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