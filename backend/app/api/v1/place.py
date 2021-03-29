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

api = Blueprint('place', __name__)


@api.route('/create', methods=['POST'])
@jwt_required
def post():
    user_curr_id = get_jwt_identity()
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")
    place_id = request.args.get('place_id', None)
    try:
        data = request.get_json()
        # Thêm id của camera
        data["cameras"]["camera_id"] = str(ObjectId())
        data["cameras"]["camera_id"] = data["cameras"]["camera_id"][:]
        #   Loại camrea
        data["cameras"]["type"] = OTHER

    except Exception as ex:
        print(ex)
        return send_error(message='Lỗi dữ liệu đầu vào')
    if place_id != '':
        try:

            key = 'cameras'
            place = client.db.place.find_one({"_id": place_id})
            if place is not None:
                if key in place:

                    place["cameras"].append(data["cameras"])
                    update_cameras = {
                        '$set': {
                            "cameras": place["cameras"]
                        }}
                    client.db.place.update_one({'_id': place_id}, update_cameras)
                else:
                    cameras = []
                    cameras.append(data["cameras"])
                    update_cameras = {
                        '$set': {
                            "cameras": cameras
                        }}
                    client.db.place.update_one({'_id': place_id}, update_cameras)

                notif = notification(
                    content="Bạn đã thêm camera " + data["cameras"]["name"] + " của " + str(data["name"]),
                    user_id=user_curr_id, type=CREATE)
                client.db.history.insert_one(notif)
            else:
                return send_error(message="Không tìm thấy địa chỉ ")
        except Exception as ex:
            print(ex)
            return send_error(message='có lỗi ngoại lệ xảy ra')

        return send_result(message="Tạo thành công ", data=place)
    else:
        try:
            cameras = []
            cameras.append(data["cameras"])
            place = {
                "_id": str(ObjectId()),
                "name": data["name"],
                "location": data["location"],
                "name_image": data["name_image"],
                "link_image": data["link_image"],
                "cameras": cameras
            }
            client.db.place.insert_one(place)
            notif = notification(
                content=claims["full_name"] + " đã thêm camera " + data["cameras"]["name"] + " của " + str(
                    data["name"]),
                user_id=user_curr_id, type=CREATE)
            client.db.history.insert_one(notif)
            return send_result(message="Tạo thành công ", data=place)
        except Exception as ex:
            print(ex)
            return send_error(message='có lỗi ngoại lệ xảy ra')


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
    place_id = request.args.get('place_id')
    camera_id = request.args.get('camera_id')

    try:
        data = request.get_json()
    except Exception as ex:
        print(ex)
        return send_error(message='Lỗi dữ liệu đầu vào')
    try:
        place = client.db.place.find_one({"_id": place_id})
        if place is not None:
            for camera in place["cameras"]:
                if camera["camera_id"] == camera_id:
                    camera_old = camera['name']
                    image_old = camera['name_image']
                    camera['name_image'] = data["cameras"]["name_image"]
                    camera['link_image'] = data["cameras"]["link_image"]
                    camera['instruction'] = data["cameras"]["instruction"]
                    camera['link_stream'] = data["cameras"]["link_stream"]
                    update_cameras = {
                        '$set': {
                            "name": data["name"],
                            "name_image": data["name_image"],
                            "link_image": data["link_image"],
                            "cameras": place["cameras"]
                        }}
                    image_camera_old = place["name_image"]
                    # Xóa file ảnh
                    if image_camera_old != data["name_image"]:
                        list_file = listdir(PATH_IMAGE_CAMERA)
                        for i in list_file:
                            if safe_str_cmp(image_camera_old, i):
                                tmp = PATH_IMAGE_CAMERA + image_camera_old
                                os.remove(tmp)
                    # Xóa file anhr camera
                    if image_old != data["cameras"]["name_image"]:
                        list_file = listdir(PATH_IMAGE_PLACE)
                        for i in list_file:
                            if safe_str_cmp(image_old, i):
                                tmp = PATH_IMAGE_PLACE + image_old
                                os.remove(tmp)
                    client.db.place.update_one({'_id': place_id}, update_cameras)
                    notif = notification(
                        content=claims["full_name"] + " đã cập nhập camera " + camera_old + " thành " + data["cameras"][
                            "name"] + " của " + str(
                            place["name"]),
                        user_id=user_curr_id, type=UPDATE)
                    client.db.history.insert_one(notif)
        else:
            return send_error(message="Không tìm thấy địa chỉ ")
    except Exception as ex:
        print(ex)
        return send_error(message='có lỗi ngoại lệ xảy ra')

    return send_result(message="Tạo user thành công ", data=client.db.place.find_one({'_id': place_id}))


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
    place_id = request.args.get('place_id')
    camera_id = request.args.get('camera_id')
    try:
        place = client.db.place.find_one({"_id": place_id})
        if place is not None:
            temp = 1
            for camera in place["cameras"]:
                if camera["camera_id"] == camera_id:
                    place["cameras"].remove(camera)
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
                        content=claims["full_name"] + " đã xóa camera " + camera["name"] + place["name"],
                        user_id=user_curr_id, type=DELETE)
                    client.db.history.insert_one(notif)
            if temp == 1:
                return send_error(message="Không tìm thấy  ")
        else:
            return send_error(message="Không tìm thấy địa chỉ ")
        update_cameras = {
            '$set': {
                "cameras": place["cameras"]
            }}
        client.db.place.update_one({'_id': place_id}, update_cameras)

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

    users = client.db.place.find().skip(skips).limit(int(page_size)).sort('_id', -1)
    '''end list'''
    list_user = list(users)
    totals = client.db.place.find().count()
    data = {
        'totals': totals,
        'results': list_user
    }
    return send_result(data=data)





@api.route('/get_by_id', methods=['GET'])
@jwt_required
def get_by_id():
    place_id = request.args.get('place_id')
    place = client.db.place.find_one({'_id': place_id})
    if not place:
        return send_error(message="Không tìm thấy bản ghi")
    data = {
        'results': place
    }
    return send_result(data=data)
