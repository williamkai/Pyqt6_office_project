# order_sorting.py
from PyQt6.QtCore import QThread, pyqtSignal

class OrderSortingThread(QThread):
    sorting_finished = pyqtSignal(dict)  # Emit a dictionary

    def __init__(self, email_data_dict, storage_path):
        super().__init__()
        self.email_data_dict = email_data_dict
        self.storage_path = storage_path

    def run(self):
        print("處理訂單整理功能")
        # 在這裡處理訂單整理
        orders = {'大榮': {}, '通盈': {}}

        # 擷取郵件內容
        for mail_id, email_content in self.email_data_dict.items():
            # print(f"Mail ID: {mail_id}, Content: {email_content}")
                
            # 按內容分類
            if '大榮' in email_content:
                order_details = self.parse_email_content(email_content)
                orders['大榮'][mail_id] = order_details

            elif '通盈' in email_content:
                order_details = self.parse_email_content(email_content)
                orders['通盈'][mail_id] = order_details
           
            # print(f"{orders}")
            # print(f"加入後的orders{orders}")
        self.sorting_finished.emit(orders)

        
    def parse_email_content(self, email_content):
        # 初始化訂單標題和商品訊息
        order_title = ""
        items = ""

        lines = email_content.split('\n')
        for line in lines:
            if "取貨明細如下：" in line:
                order_title=line
                break
        order_title=self.parse_order_title(order_title)

        items=self.parse_order_items(lines)

        return {
            'title': order_title,
            'items': items
            }
    
    def parse_order_title(self, extracted_text):
        # 指定要移除的字元
        remove_markers = ['大榮-', '通盈-','-']
        extracted_text
        detail_marker_1 = '衛生紙訂單'
        detail_index_1 = extracted_text.find(detail_marker_1)
        detail_marker_2 = '宅配訂單'
        detail_index_2 = extracted_text.find(detail_marker_2)
        detail_marker_3 = '訂單'
        detail_index_3 = extracted_text.find(detail_marker_3)
        detail_marker_4 = '衛生紙'
        detail_index_4 = extracted_text.find(detail_marker_4)

        if detail_index_1 != -1:
            # 擷取“取貨明細如下：”之前的內容
            pre_detail_content = extracted_text[:detail_index_1].strip()
            pre_detail_content = self.remove_markers_from_text(pre_detail_content, remove_markers)

            # # 移除指定的字元
            # for marker in remove_markers:
            #     pre_detail_content = pre_detail_content.replace(marker, '')

            # 清理前後的空白字符
            pre_detail_content = pre_detail_content.strip()

            # 判斷第一個字是不是 '0'，如果是 '0' 就移除
            if pre_detail_content and pre_detail_content[0] == '0':
                pre_detail_content = pre_detail_content[1:].strip()
            return pre_detail_content
        
        elif detail_index_2 != -1:
            # 擷取“取貨明細如下：”之前的內容
            pre_detail_content = extracted_text[:detail_index_2].strip()

            pre_detail_content = self.remove_markers_from_text(pre_detail_content, remove_markers)

            # 判斷第一個字是不是 '0'，如果是 '0' 就移除
            if pre_detail_content and pre_detail_content[0] == '0':
                pre_detail_content = pre_detail_content[1:].strip()
            return pre_detail_content

        elif detail_index_3 != -1:
            # 擷取“取貨明細如下：”之前的內容
            pre_detail_content = extracted_text[:detail_index_3].strip()
            pre_detail_content = self.remove_markers_from_text(pre_detail_content, remove_markers)

            # 判斷第一個字是不是 '0'，如果是 '0' 就移除
            if pre_detail_content and pre_detail_content[0] == '0':
                pre_detail_content = pre_detail_content[1:].strip()
            return pre_detail_content
        
        elif detail_index_4 != -1:
            # 擷取“取貨明細如下：”之前的內容
            pre_detail_content = extracted_text[:detail_index_4].strip()
            pre_detail_content = self.remove_markers_from_text(pre_detail_content, remove_markers)
            # 判斷第一個字是不是 '0'，如果是 '0' 就移除
            if pre_detail_content and pre_detail_content[0] == '0':
                pre_detail_content = pre_detail_content[1:].strip()
            return pre_detail_content

        else:
            print("未找到匹配的文字")
            return ""
    
    def remove_markers_from_text(self,text, markers):
        """
        移除指定字元
        """
        for marker in markers:
            text = text.replace(marker, '')
        return text.strip()

    def parse_order_items(self,order_lines):
        # 初始化变量
        start_marker = '取貨明細如下'
        end_marker = '以上'
        start_index = None
        end_index = None

        # 找到"取貨明細如下："和"以上"的行索引
        for i, line in enumerate(order_lines):
            if start_marker in line:
                start_index = i
            if end_marker in line:
                end_index = i
                break

        # 如果找到有效的起始和结束行
        if start_index is not None and end_index is not None:
            # 提取"取貨明細如下："和"以上"之间的内容
            detail_lines = order_lines[start_index + 1:end_index]
            # 处理每一行
            items = []
            for line in detail_lines:
                line = line.strip()
                if line.endswith('箱'):
                # 倒序查找最后一个 '…'
                    product_code, separator, remaining = line.rpartition('…')

                    # 去掉商品数量中的“箱”并去除空格
                    quantity = remaining.replace('箱', '').strip()

                    # 移除 product_code 中剩余的 '…' 并去除空格
                    product_code = product_code.replace('…', '').strip()

                    # 将结果添加到 items 列表中
                    items.append({'product_code': product_code, 'quantity': quantity})
            return items