from os import listdir
import os
from flask import Blueprint, request
from werkzeug.security import safe_str_cmp

from app.enums import USER_ACTIVATED, USER_DEACTIVATED, STATUS_USER, CREATE, DELETE, UPDATE, POLICE, PATH_IMAGE_CAMERA
from app.utils import  send_result, send_error, notification
from app.extensions import client
from bson import ObjectId
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity)

api = Blueprint('police', __name__)


@api.route('/create', methods=['POST'])
@jwt_required
def post():
    user_curr_id = get_jwt_identity()
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")
    police_id = request.args.get('police_id')
    try:
        data = request.get_json()
        # Thêm id của camera
        data["cameras"]["camera_id"] = str(ObjectId())
        data["cameras"]["camera_id"] = data["cameras"]["camera_id"][:]
        # Loại camrea
        data["cameras"]["type"] = POLICE

    except Exception as ex:
        print(ex)
        return send_error(message='Lỗi dữ liệu đầu vào')
    try:

        key = 'cameras'
        police = client.db.police.find_one({"_id": police_id})
        if police is not None:
            if key in police:

                police["cameras"].append(data["cameras"])
                update_cameras = {
                    '$set': {
                        "cameras": police["cameras"]
                    }}
                client.db.police.update_one({'_id': police_id}, update_cameras)
            else:
                cameras = []
                cameras.append(data["cameras"])
                update_cameras = {
                    '$set': {
                        "cameras": cameras
                    }}
                client.db.police.update_one({'_id': police_id}, update_cameras)

            notif = notification(content=claims["full_name"] + " đã thêm camera " + data["cameras"]["name"] + " của " + str(data["name"]),
                                 user_id=user_curr_id,type=CREATE)
            client.db.history.insert_one(notif)
        else:
            return send_error(message="Không tìm thấy địa chỉ ")
    except Exception as ex:
        print(ex)
        return send_error(message='có lỗi ngoại lệ xảy ra')

    return send_result(message="Tạo thành công ", data=police)


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
    police_id = request.args.get('police_id')
    camera_id = request.args.get('camera_id')

    try:
        data = request.get_json()
    except Exception as ex:
        print(ex)
        return send_error(message='Lỗi dữ liệu đầu vào')
    try:
        police = client.db.police.find_one({"_id": police_id})
        if police is not None:
            for camera in police["cameras"]:
                if camera["camera_id"] == camera_id:
                    camera_old = camera['name']
                    image_old = camera['photo']
                    camera['name'] = data["cameras"]["name"]
                    camera['name_image'] = data["cameras"]["name_image"]
                    camera['link_image'] = data["cameras"]["link_image"]
                    camera['instruction'] = data["cameras"]["instruction"]
                    camera['link_stream'] = data["cameras"]["link_stream"]
                    update_cameras = {
                        '$set': {
                            "cameras": police["cameras"]
                        }}
                    if image_old != data["cameras"]["name_image"]:
                        list_file = listdir(PATH_IMAGE_CAMERA)
                        for i in list_file:
                            if safe_str_cmp(image_old, i):
                                tmp = PATH_IMAGE_CAMERA + image_old
                                os.remove(tmp)
                    client.db.police.update_one({'_id': police_id}, update_cameras)
                    notif = notification(content=claims["full_name"] + " đã cập nhập camera " + camera_old + " thành " + data["cameras"][
                        "name"] + " của " + str(police["name"]),
                                         user_id=user_curr_id, type=UPDATE)
                    client.db.history.insert_one(notif)
        else:
            return send_error(message="Không tìm thấy địa chỉ ")

    except Exception as ex:
        print(ex)
        return send_error(message='có lỗi ngoại lệ xảy ra')

    return send_result(message="Tạo user thành công ", data=client.db.police.find_one({'_id':police_id}))

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
    police_id = request.args.get('police_id')
    camera_id = request.args.get('camera_id')
    try:
        police = client.db.police.find_one({"_id": police_id})
        if police is not None:
            temp = 1
            for camera in police["cameras"]:
                if camera["camera_id"] == camera_id:
                    police["cameras"].remove(camera)
                    temp = 0
                    # Xoa file
                    try:
                        list_file = listdir(PATH_IMAGE_CAMERA)
                        for i in list_file:
                            if safe_str_cmp(camera["name_image"], i):
                                tmp = PATH_IMAGE_CAMERA + camera["name_image"]
                                os.remove(tmp)
                    except Exception as ex:
                        return send_error(message="Xóa tệp không thành công")
                    notif = notification(
                        content=claims["full_name"] + " đã xóa camera " + camera["name"] + police["name"],
                        user_id=user_curr_id, type=DELETE)
                    client.db.history.insert_one(notif)
            if temp == 1:
                return send_error(message="Không tìm thấy  ")
        else:
            return send_error(message="Không tìm thấy địa chỉ ")
        update_cameras = {
            '$set': {
                "cameras": police["cameras"]
            }}
        client.db.police.update_one({'_id': police_id}, update_cameras)

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

    users = client.db.police.find().skip(skips).limit(int(page_size)).sort('_id', -1)
    '''end list'''
    list_user = list(users)
    totals = client.db.police.find().count()
    data = {
        'totals': totals,
        'results': list_user
    }
    return send_result(data=data)



@api.route('/get_by_id', methods=['GET'])
@jwt_required
def get_by_id():
    police_id = request.args.get('police_id')
    police = client.db.police.find_one({'_id':police_id})
    if not police:
        return send_error(message="Không tìm thấy bản ghi")
    data = {
        'results': police
    }
    return send_result(data=data)
