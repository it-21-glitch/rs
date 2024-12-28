from flask import Flask
from flask_wtf import CSRFProtect
from .settings import audit_status


def create_flask_app(classobj):
    # 启动配置
    flask_app = Flask(__name__, static_folder='../static', template_folder='../templates')  # 启动对象
    flask_app.config.from_object(classobj)  # 类加载配置
    flask_app.add_template_filter(audit_status, 'audit')  # 将过滤器函数注册
    csrf = CSRFProtect()  # 3.实例化csrf
    csrf.init_app(flask_app)  # 4.将app注册
    return flask_app  # 返回flask框架的app对象
