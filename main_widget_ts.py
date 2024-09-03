import os
from datetime import datetime
import xlwings as xw  # 確保已經安裝 xlwings

def generate_file_name():
    now = datetime.now()
    year = now.year - 1911  # 假設你需要的年份是民國年份
    month = now.month
    file_name = f"{year}年{month}月久富餘對帳明細表-菁弘(含退貨).xlsx"
    return file_name

# 調用 generate_file_name 函數並打印結果
file_name = generate_file_name()
print(f"{file_name}")
