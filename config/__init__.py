from .app import create_flask_app
from .db_config import get_db
from .settings import DevelopmentConfig, VerifyForm, VerifyUpdateForm, regular_function, rule_data_base, audit_status, \
    generation_xlsx

app = create_flask_app(DevelopmentConfig)
__all__ = ['app', 'VerifyForm', 'get_db', "VerifyUpdateForm", 'regular_function', 'rule_data_base', 'audit_status',
           'generation_xlsx']
