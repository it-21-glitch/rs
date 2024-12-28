from flask import Blueprint
from blueprints.factory import *
from blueprints.rs import *

rs_bp = Blueprint('rs', __name__, url_prefix='/rs')
factory_bp = Blueprint('factory', __name__, url_prefix='/')

rs_bp.add_url_rule(
    rule='/login',
    endpoint='rs_login',
    view_func=rs_login,
    methods=["GET", "POST"]
)
rs_bp.add_url_rule(
    rule='/logout',
    endpoint='rs_logout',
    view_func=rs_logout,
    methods=["DELETE"]
)

rs_bp.add_url_rule(
    rule='/rs_index',
    endpoint='rs_index',
    view_func=rs_index,
    methods=["GET"]
)
rs_bp.add_url_rule(
    rule='/rs_upload_attendance',
    endpoint='rs_upload_attendance',
    view_func=rs_upload_attendance,
    methods=["POST"]
)

rs_bp.add_url_rule(
    rule='/rs_to_examine',
    endpoint='rs_to_examine',
    view_func=rs_to_examine,
    methods=["POST"]
)

rs_bp.add_url_rule(
    rule='/rs_sign_in_record',
    endpoint='rs_sign_in_record',
    view_func=rs_sign_in_record,
    methods=["GET"]
)
rs_bp.add_url_rule(
    rule='/rs_to_examine',
    endpoint='rs_to_examine',
    view_func=rs_to_examine,
    methods=["POST"]
)
rs_bp.add_url_rule(
    rule='/rs_to_examine_all',
    endpoint='rs_to_examine_all',
    view_func=rs_to_examine_all,
    methods=["POST"]
)


__all__ = [
    "rs_bp",
    "factory_bp",
]
