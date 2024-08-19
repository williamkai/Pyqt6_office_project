# email_search_thread.py
from email.header import Header
from email.header import decode_header
import re
import imaplib
import email
from PyQt6.QtCore import QThread, pyqtSignal

class EmailSearchThread(QThread):

    search_finished = pyqtSignal(list, dict)  # Emit list of tuples with (mail_id, email_message)

    def __init__(self, email, password,search_criteria,keyword):
        super().__init__()
        self.email = email
        self.password = password
        self.search_criteria = search_criteria
        self.keyword=keyword

    def run(self):
        mail_data = {}
        displayed_items = []
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.email, self.password)
            mail.select('inbox')

            print(f"搜索條件: {self.search_criteria}")
            result, data = mail.search(None,self.search_criteria)
            if result == 'OK':
                mail_ids = data[0].split()
                print(f"找到的郵件數量: {len(mail_ids)}")
                for mail_id in mail_ids:
                    result, message_data = mail.fetch(mail_id, '(RFC822)')
                    raw_email = message_data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                     # 直接解碼標題
                    subject = email_message.get('Subject', '(無標題)')
                    subject = self.decode_mime_header(subject) if subject else "(無標題)"
                    subject = self.clean_email_subject_content(subject)
                    email_content=self.extract_order_details(email_message)

                    self_keyword = self.keyword.lower()
                    subject_lower = subject.lower()

                    # 定义排除的关键字列表
                    exclude_keywords = ["退订", "回收", "re"]

                    # 检查排除关键字是否存在于主题中
                    exclude_condition = any(exclude_kw.lower() in subject_lower for exclude_kw in exclude_keywords)
   
                    # 判断是否需要执行
                    if self_keyword in subject_lower and not exclude_condition:
                        displayed_items.append((mail_id, f"標題:{subject} (信件代號:{mail_id})"))
                        mail_data[mail_id] = email_content

            mail.logout()

        except Exception as e:
            print(f"Error: {e}")

        self.search_finished.emit(displayed_items, mail_data)

    def decode_mime_header(self, header):
        decoded_parts = decode_header(header)
        decoded_string = ""
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):  # 檢查 part 是否爲 bytes 類型
                # 如果是 bytes 類型，則進行解碼
                decoded_string += part.decode(encoding if encoding else 'utf-8', errors='replace')
            else:
                # 如果是 str 類型，直接添加到結果中
                decoded_string += part
        
        return decoded_string
    
    def extract_order_details(self, email_message):
        email_content = ""
        attachment_info = []

        # 取得接收時間
        date_header = email_message.get('Date', '')

        # 解析郵件內容
        if email_message.is_multipart():
            for part in email_message.walk():
                # 首先判斷是否是附件
                if part.get('Content-Disposition') is not None:
                    filename = part.get_filename()
                    if filename:
                        decoded_filename = self.decode_mime_header(filename)
                        attachment_info.append(decoded_filename)
                    continue  # 是附件就跳過這次迴圈，避免進一步處理這部分的內文

                # 處理內文內容
                content_type = part.get_content_type()
                charset = part.get_content_charset()
                
                if content_type == "text/plain":
                    try:
                        payload = part.get_payload(decode=True)
                        if charset:
                            email_content += payload.decode(charset)
                        else:
                            email_content += payload.decode('utf-8', errors='replace')
                    except (UnicodeDecodeError, TypeError) as e:
                        print(f"解碼錯誤: {e}")

        else:
            charset = email_message.get_content_charset()
            try:
                payload = email_message.get_payload(decode=True)
                if charset:
                    email_content = payload.decode(charset)
                else:
                    email_content = payload.decode('utf-8', errors='replace')
            except (UnicodeDecodeError, TypeError) as e:
                print(f"解碼錯誤: {e}")

        # 清理郵件內容，去掉 "Subject:" 行及其以上的部分
        email_content = self.clean_email_content(email_content)

        if attachment_info:
                email_content += "\n\n附件:\n"
                for attachment in attachment_info:
                    email_content += f"- {attachment}\n"
            
        # 添加接收時間到郵件內容中
        if date_header:
            email_content = f"接收時間: {date_header}\n\n{email_content}"



        return email_content
    
    def clean_email_content(self,content):
        # 查找并删除从 "Subject:" 行到邮件开头的部分
        pattern = r'Subject:.*\n.*\n'
        match = re.search(pattern, content)
        if match:
            # 找到 "Subject:" 行的位置，删除其以上内容
            content = content[match.end():].strip()
        return content
    
    def clean_email_subject_content(self,subject):
        subject=subject.replace("FW:", '')
        return subject
