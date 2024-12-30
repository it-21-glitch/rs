from flask import Blueprint
from blueprints.factory import *
from blueprints.rs import *

rs_bp = Blueprint('rs', __name__, url_prefix='/rs')
factory_bp = Blueprint('factory', __name__, url_prefix='/')

#  rs +++++++++++++++++++++
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

# factory +++++++++++++++++++++++++++
factory_bp.add_url_rule(
    rule='/',
    endpoint='factory_index',
    view_func=factory_index,
    methods=["GET"]
)

factory_bp.add_url_rule(
    rule='/factory_add_records',
    endpoint='factory_add_records',
    view_func=factory_add_records,
    methods=["GET"]
)

factory_bp.add_url_rule(
    rule='/factory_get_equipment_and_process',
    endpoint='factory_get_equipment_and_process',
    view_func=factory_get_equipment_and_process,
    methods=["GET"]
)
factory_bp.add_url_rule(
    rule='/factory_get_attendance_and_production_records',
    endpoint='factory_get_attendance_and_production_records',
    view_func=factory_get_attendance_and_production_records,
    methods=["POST"]
)
factory_bp.add_url_rule(
    rule='/factory_download_attendance_and_production_records',
    endpoint='factory_download_attendance_and_production_records',
    view_func=factory_download_attendance_and_production_records,
    methods=["GET"]
)
factory_bp.add_url_rule(
    rule='/factory_get_information_description',
    endpoint='factory_get_information_description',
    view_func=factory_get_information_description,
    methods=["GET"]
)

factory_bp.add_url_rule(
    rule='/factory_add_record',
    endpoint='factory_add_record',
    view_func=factory_add_record,
    methods=["POST"]
)

factory_bp.add_url_rule(
    rule='/factory_add_user',
    endpoint='factory_add_user',
    view_func=factory_add_user,
    methods=["POST"]
)

factory_bp.add_url_rule(
    rule='/factory_download_template_file_roster',
    endpoint='factory_download_template_file_roster',
    view_func=factory_download_template_file_roster,
    methods=["GET"]
)

factory_bp.add_url_rule(
    rule='/factory_delete_attendance_and_production_records',
    endpoint='factory_delete_attendance_and_production_records',
    view_func=factory_delete_attendance_and_production_records,
    methods=["DELETE"]
)
__all__ = [
    "rs_bp",
    "factory_bp",
]
