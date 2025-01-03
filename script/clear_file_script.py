import os
import smtplib
from datetime import date
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from concurrent.futures import ThreadPoolExecutor


def send_email(remove_list):
    # 获取当前日期
    today = date.today()
    # 获取年、月、日
    year = today.year
    month = today.month
    day = today.day
    # 发件人和收件人信息
    sender_email = "it-19@1bizmail.com"
    receiver_email = "it-21@1bizmail.com"  # 收件人
    password = "like+1314"

    # 创建邮件
    message = MIMEMultipart()
    message["From"] = Header('[RS]系统管理员', 'utf-8')
    message["To"] = receiver_email
    message["Subject"] = "系统文件检测"
    message["Accept-Language"] = "zh-CN"
    message["Accept-Charset"] = "utf-8"
    # 添加邮件正文
    message.attach(MIMEText("根据关键字检测请留意以下文件:<br/>&nbsp" + ',<br/>&nbsp'.join(
        remove_list) + f"<div style='float: right;margin-top: 10px;'>日期:{year}年{month}月{day}日</div>", "html"))

    # 连接到SMTP服务器
    with smtplib.SMTP("exchange.1bizmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("邮件已发送成功！")


def delete_files_with_keywords(directory, keywords):
    """
    扫描磁盘并删除包含特定关键字的文件
    """
    remove_list = []
    with ThreadPoolExecutor() as executor:
        # 定义一个辅助函数，用于检查文件名是否包含关键字
        def check_file(file):
            return any(keyword in file for keyword in keywords)

        # 定义一个辅助函数，用于收集需要删除的文件
        def collect_files(root, files):
            file_path_list = []
            for file in files:
                if check_file(file):
                    file_path = os.path.join(root, file)
                    file_path_list.append(file_path)
            return file_path_list

        # 并行扫描目录
        futures = [executor.submit(collect_files, root, files) for root, _, files in os.walk(directory)]
        for future in futures:
            remove_list.extend(future.result())

    send_email(remove_list)


base_path = os.path.abspath(os.path.dirname(__file__))
conf_path = os.path.join(base_path, 'clear.conf')
with open(conf_path,mode='r',encoding='utf-8') as f:
    a = f.read()
    print(a)
# # 定义关键字
# keywords = ["订单", "外发", "工厂采购单"]
# future_path = f'C:\\Users\\Administrator\\Desktop\\test'
# # 调用函数
# delete_files_with_keywords(future_path, keywords)

# pyinstaller -F 123.py 打包即可
