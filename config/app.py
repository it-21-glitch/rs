import os
from flask import Flask
from flask_wtf import CSRFProtect
from .settings import audit_status

PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def create_flask_app(classobj):
    # 启动配置
    flask_app = Flask(__name__, static_folder='../static', template_folder='../templates')  # 启动对象
    flask_app.config.from_object(classobj)  # 类加载配置
    flask_app.add_template_filter(audit_status, 'audit')  # 将过滤器函数注册
    csrf = CSRFProtect()  # 3.实例化csrf
    csrf.init_app(flask_app)  # 4.将app注册
    # 检测文件夹
    generation_xlsx = os.path.join(PATH, 'static', "generation_xlsx")
    attendance_picture = os.path.join(PATH, 'static', "attendance_picture")
    logs = os.path.join(PATH, 'logs')

    if not os.path.exists(generation_xlsx):
        os.mkdir(generation_xlsx)

    if not os.path.exists(attendance_picture):
        os.mkdir(attendance_picture)

    if not os.path.exists(logs):
        os.mkdir(logs)
    return flask_app  # 返回flask框架的app对象
