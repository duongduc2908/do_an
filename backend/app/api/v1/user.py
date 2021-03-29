from flask import Blueprint, request
from app.enums import USER_ACTIVATED, USER_DEACTIVATED, STATUS_USER,CREATE,UPDATE,DELETE
from app.utils import parse_req, FieldString, send_result, send_error, hash_password, set_auto_MaNV, notification
from app.extensions import client
from bson import ObjectId
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity)

api = Blueprint('user', __name__)

"""
Function: User registration - Admin right required
Input: user_name, password, email, fullname, group_role_id
Output: Success / Error Message
"""


@api.route('/create', methods=['POST'])
@jwt_required
def post():
    user_curr_id = get_jwt_identity()
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")

    params = {
        'user_name': FieldString(requirement=True),
        'password': FieldString(requirement=True),
        'email': FieldString(requirement=True),
        'full_name': FieldString(requirement=True),
        'group_role_id': FieldString(requirement=True)
    }

    try:
        json_data = parse_req(params)
        full_name = json_data.get('full_name', None)
        email = json_data.get('email', None).lower()
        user_name = json_data.get('user_name', None)
        password = json_data.get('password', None)
        group_role_id = json_data.get('group_role_id', '0')
    except Exception:
        return send_error(message='Lỗi dữ liệu đầu vào')

    '''check conditions'''

    '''end check'''

    '''create MNV auto'''

    '''end create MNv'''
    _id = str(ObjectId())
    user = {
        '_id': _id,
        'full_name': full_name,
        'user_name': user_name,
        'password': hash_password(password),
        'email': email,
        'group_role_id': group_role_id,
        'status': USER_ACTIVATED,
        'MaNV': set_auto_MaNV()
    }
    try:
        client.db.user.insert_one(user)
        notif = notification(content=claims['full_name']+" đã thêm nhân viên " + full_name + " thành công", user_id=user_curr_id, type=CREATE)
        client.db.history.insert_one(notif)
    except Exception as ex:
        print(ex)
        return send_error(message='có lỗi ngoại lệ xảy ra')

    return send_result(message="Tạo user thành công ", data=user)


"""
Function: Update user's profile - Admin right required
Input: user_id
Output: Success / Error Message
"""


@api.route('/update', methods=['PUT'])
@jwt_required
def put():
    user_curr_id = get_jwt_identity()
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")

    user_id = request.args.get('user_id')
    user = client.db.user.find_one({'_id': user_id})
    if user is None:
        return send_error(message='Không tìm thấy người dùng.')

    params = {
        'user_name': FieldString(requirement=True),
        'password': FieldString(requirement=True),
        'email': FieldString(requirement=True),
        'full_name': FieldString(requirement=True),
        'group_role_id': FieldString(requirement=True),
        'status': FieldString(requirement=True),
    }

    try:
        json_data = parse_req(params)
        full_name = json_data.get('full_name', None)
        email = json_data.get('email', None).lower()
        user_name = json_data.get('user_name', None)
        password = json_data.get('password', None)
        group_role_id = json_data.get('group_role_id', '0')
        status = json_data.get('status', '0')


    except Exception:
        return send_error(message='Lỗi dữ liệu đầu vào')
    '''Check '''
    if status == USER_ACTIVATED:
        status = USER_ACTIVATED
    elif status == USER_DEACTIVATED:
        status = USER_DEACTIVATED
    else:
        return send_error(message="Bạn chưa nhập trạng thái")
    '''End check'''
    _id = str(ObjectId())
    new_user = {
        '$set': {
            'full_name': full_name,
            'user_name': user_name,
            'password': hash_password(password),
            'email': email,
            'group_role_id': group_role_id,
            'status': status,
        }}
    try:
        client.db.user.update_one({'_id': user_id}, new_user)
        notif = notification(content=claims['full_name']+" đã sửa nhân viên " + full_name + " thành công", user_id=user_curr_id, type=UPDATE)
        client.db.history.insert_one(notif)
    except Exception as ex:
        print(ex)
        return send_error(message='có lỗi ngoại lệ sảy ra')
    return send_result(message="Cập nhật thành công", data=client.db.user.find_one({'_id':user_id}))


"""
Function: Update user's profile - Admin right required
Input: user_id
Output: Success / Error Message
"""


@api.route('/delete', methods=['DELETE'])
@jwt_required
def delete():
    user_curr_id = get_jwt_identity()
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")
    user_id = request.args.get('user_id')
    user = client.db.user.find_one({'_id': user_id})
    if user is None:
        return send_error(message="Không tìm thấy dự liệu đầu vào trong cơ sở dữ liệu")
    try:
        client.db.user.delete_one({'_id': user_id})
        notif = notification(content=claims['full_name']+" đã xóa nhân viên " + user['full_name'] + " thành công", user_id=user_curr_id,type=DELETE)
        client.db.history.insert_one(notif)
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
    text_search = request.args.get('text_search', '')
    page_size = request.args.get('page_size', '25')
    page_number = request.args.get('page_number', '0')
    skips = int(page_size) * int(page_number)
    '''Give list after filtering'''
    query = \
        {'$and': [
            {'status': USER_ACTIVATED},
            {'$or': [
                {'email': {'$regex': text_search, '$options': "$i"}},
                {'MaNV': {'$regex': text_search, '$options': "$i"}},
                {'full_name': {'$regex': text_search, '$options': "$i"}}
            ]}
        ]}
    users = client.db.user.find(query).skip(skips).limit(int(page_size))
    '''end list'''
    list_user = list(users)
    '''Make a request'''

    for i in list_user:
        if int(i['status']) == USER_ACTIVATED:
            i['status_name'] = STATUS_USER[USER_ACTIVATED]
        if int(i['status']) == USER_DEACTIVATED:
            i['status_name'] = STATUS_USER[USER_DEACTIVATED]
    '''end request'''
    totals = client.db.user.find().count()
    data = {
        'totals': totals,
        'results': list_user
    }
    return send_result(data=data)


"""
Function: Get all page
Input: 
Output: Success / Error Message
"""


@api.route('/get_all_page', methods=['GET'])
# @jwt_required
def get_all_page():
    page_size = 25#request.args.get('page_size', '25')
    page_number = 0#request.args.get('page_number', '0')
    skips = int(page_size) * int(page_number)
    users = client.db.user.find().skip(skips).limit(int(page_size)).sort('_id', -1)
    list_user = list(users)
    '''Make a request'''

    for i in list_user:
        if int(i['status']) == USER_ACTIVATED:
            i['status_name'] = STATUS_USER[USER_ACTIVATED]
        if int(i['status']) == USER_DEACTIVATED:
            i['status_name'] = STATUS_USER[USER_DEACTIVATED]
    '''end request'''
    totals = client.db.user.find().count()
    data = {
        'totals': totals,
        'results': list_user
    }
    return send_result(data=data)

"""
Function: Get by_ id
Input: 
Output: Success / Error Message
"""

@api.route('/get_by_id', methods=['GET'])
@jwt_required
def get_by_id():
    user_id = request.args.get('user_id')
    users = client.db.user.find_one({'_id': user_id})
    if not users:
        return send_error(message="Không tìm thấy bản ghi")
    data = {
        'results': users
    }
    return send_result(data=data)
