import os
import smtplib
from datetime import date
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
    message.attach(MIMEText("根据关键字检测请留意以下文件:<br/>&nbsp"+',<br/>&nbsp'.join(remove_list) + f"<div style='float: right;margin-top: 10px;'>日期:{year}年{month}月{day}日</div>", "html"))

    # 连接到SMTP服务器
    with smtplib.SMTP("exchange.1bizmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("邮件已发送成功！")


def delete_files_with_keywords(directory, keywords):
    """
        扫描磁盘
    """
    remove_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if any of the keywords are in the filename
            if any(keyword in file for keyword in keywords):
                file_path = os.path.join(root, file)
                remove_list.append(file_path)
            # 删除C盘根目录下文件名包含“订单”或“外发”的文件
    print(remove_list)
    send_email(remove_list)


keywords = ["订单", "外发", "工厂采购单"]
delete_files_with_keywords('C:\\Users\\Administrator\\Desktop\\test', keywords)
# delete_files_with_keywords('C:\\', keywords)
