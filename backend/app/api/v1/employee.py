from os import listdir

from flask import Blueprint, request
from werkzeug.security import safe_str_cmp
import os
from app.enums import USER_ACTIVATED, USER_DEACTIVATED, STATUS_USER, CREATE, DELETE, UPDATE, OTHER, PATH_CAMERA, \
    PATH_IMAGE_CAMERA, PATH_IMAGE_PLACE
from app.utils import send_result, send_error, notification
from app.extensions import client
from bson import ObjectId
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity)

api = Blueprint('employee', __name__)


@api.route('/create', methods=['POST'])
@jwt_required
def post():
    user_curr_id = get_jwt_identity()
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")
    try:
        data = request.get_json()
    except Exception as ex:
        print(ex)
        return send_error(message='Lỗi dữ liệu đầu vào')
    try:
        department = {
            "e_id": str(ObjectId()),
            "e_code": data["e_code"],
            "e_name": data["e_name"],
            "e_description": data["e_description"],
            "e_note": data["e_note"],
            "e_address":data["e_address"]

        }
        client.db.department.insert_one(department)
        notif = notification(
            content=claims["full_name"] + " đã thêm phong ban " + data["dp_name"],
            user_id=user_curr_id, type=CREATE)
        client.db.history.insert_one(notif)
        return send_result(message="Tạo thành công ", data=data)
    except Exception as ex:
        print(ex)
        return send_error(message='có lỗi ngoại lệ xảy ra')


"""
Function: Update department's - Admin right required
Input: udp_id
Output: Success / Error Message
"""


@api.route('/update', methods=['PUT'])
@jwt_required
def put():
    user_curr_id = get_jwt_identity()
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")
    dp_id = request.args.get('dp_id')

    try:
        data = request.get_json()
    except Exception as ex:
        print(ex)
        return send_error(message='Lỗi dữ liệu đầu vào')
    try:
        department = client.db.department.find_one({"dp_id": dp_id})
        if department is not None:
            update_department = {
                        '$set': {
                            "dp_code": data["dp_code"],
                            "dp_name": data["dp_name"],
                            "dp_description": data["dp_description"],
                            "dp_note": data["dp_note"]
                        }}
            client.db.department.update_one({'dp_id': dp_id}, update_department)
            notif = notification(
                content=claims["full_name"] + " đã cập nhập thong tin " + department["dp_name"],
                user_id=user_curr_id, type=UPDATE)
            client.db.history.insert_one(notif)
            return send_result(message="Tạo department thành công ", data=data)
        else:
            return send_error(message="Không tìm thấy phong ban ")
    except Exception as ex:
        print(ex)
        return send_error(message='có lỗi ngoại lệ xảy ra')
    


"""
Function: Delete department's - Admin right required
Input: dp_id
Output: Success / Error Message
"""


@api.route('/delete', methods=['DELETE'])
@jwt_required
def delete():
    user_curr_id = get_jwt_identity()
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")
    dp_id = request.args.get('dp_id')
    try:
        department = client.db.department.find_one({"dp_id": dp_id})
        if department is not None:
            client.db.department.delete(dp_id)
            notif = notification(
                content=claims["full_name"] + " đã xóa phong ban " +department["dp_name"],
                user_id=user_curr_id, type=DELETE)
            client.db.history.insert_one(notif)
        else:
            return send_error(message="Không tìm thấy phong ban ")
    except Exception:
        return send_error(message="Lỗi xóa không thành công")

    return send_result(message="Xóa thành công")


"""
Function: Get all page
Input: 
Output: Success / Error Message
"""


@api.route('/get_all_page_search', methods=['GET'])
@jwt_required
def get_all_page_search():
    page_size = request.args.get('page_size', '25')
    page_number = request.args.get('page_number', '0')
    skips = int(page_size) * int(page_number)
    '''Give list after filtering'''

    departments = client.db.department.find().skip(skips).limit(int(page_size)).sort('dp_id', -1)
    '''end list'''
    list_department = list(departments)
    totals = client.db.department.find().count()
    data = {
        'totals': totals,
        'results': list_department
    }
    return send_result(data=data)





@api.route('/get_by_id', methods=['GET'])
@jwt_required
def get_by_id():
    department_id = request.args.get('dp_id')
    department = client.db.department.find_one({'dp_id': department_id})
    if not place:
        return send_error(message="Không tìm thấy bản ghi")
    data = {
        'results': department
    }
    return send_result(data=data)
