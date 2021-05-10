from flask import request, Blueprint
import datetime
from app.enums import PATH_CAMERA, PATH_CAMERA_SEVER, PATH_IMAGE_PLACE, PATH_IMAGE_PLACE_SEVER, PATH_IMAGE_CAMERA, \
    PATH_IMAGE_CAMERA_SEVER
from app.utils import send_result, send_error
import os
from os import listdir
from werkzeug.utils import secure_filename
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims)

api = Blueprint('file', __name__)


@api.route('/file_camera', methods=['POST'])
@jwt_required
def upload_camera():
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")

    try:
        file = request.files['file']
    except Exception:
        return send_error(message='Không có file nào được chọn')
    filename = datetime.datetime.now().strftime("%f")+file.filename
    filename = secure_filename(filename)
    list_file = listdir(PATH_CAMERA)
    for i in list_file:
        if safe_str_cmp(filename, i):
            return send_error(message="Tên file đã tồn tại, bạn có muốn thay thế file cũ không?")
    try:
        file.save(os.path.join(PATH_CAMERA, filename))
        path_server = os.path.join(PATH_CAMERA_SEVER, filename)
        data = {
            'filename': filename,
            'link': path_server
        }
        return send_result(data=data, message='Tải file thành công')
    except Exception as ex:
        return send_error(message='File chưa được upload')

        
@api.route('/place_image', methods=['POST'])
@jwt_required
def upload_image_place():
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")

    try:
        file = request.files['file']
    except Exception:
        return send_error(message='Không có file nào được chọn')
    filename = datetime.datetime.now().strftime("%f")+file.filename
    filename = secure_filename(filename)
    list_file = listdir(PATH_IMAGE_PLACE)
    for i in list_file:
        if safe_str_cmp(filename, i):
            return send_error(message="Tên file đã tồn tại, bạn có muốn thay thế file cũ không?")
    try:
        file.save(os.path.join(PATH_IMAGE_PLACE, filename))
        path_server = os.path.join(PATH_IMAGE_PLACE_SEVER, filename)
        data = {
            'name_image': filename,
            'link_image': path_server
        }
        return send_result(data=data, message='Tải file thành công')
    except Exception as ex:
        return send_error(message='File chưa được upload')


@api.route('/camera_image', methods=['POST'])
@jwt_required
def upload_image_camera():
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")

    try:
        file = request.files['file']
    except Exception:
        return send_error(message='Không có file nào được chọn')
    filename = datetime.datetime.now().strftime("%f")+file.filename
    filename = secure_filename(filename)
    list_file = listdir(PATH_IMAGE_CAMERA)
    for i in list_file:
        if safe_str_cmp(filename, i):
            return send_error(message="Tên file đã tồn tại, bạn có muốn thay thế file cũ không?")
    try:
        file.save(os.path.join(PATH_IMAGE_CAMERA, filename))
        path_server = os.path.join(PATH_IMAGE_CAMERA_SEVER, filename)
        data = {
            'name_image': filename,
            'link_image': path_server
        }
        return send_result(data=data, message='Tải file thành công')
    except Exception as ex:
        return send_error(message='File chưa được upload')


@api.route('/upload_train', methods=['POST'])
@jwt_required
def upload_train():
    claims = get_jwt_claims()
    if not claims['is_admin']:
        return send_error(message="Bạn không đủ quyền để thực hiện thao tác này")

    try:
        # print(files)
        file = request.files['file']
    except Exception as e:
        print(e)
        return send_error(message='Không có file nào được chọn')
    filename = datetime.datetime.now().strftime("%f")+file.filename
    filename = secure_filename(filename)
    file.save(os.path.join(PATH_IMAGE_CAMERA, filename))
    return send_result(message='Tải file thành công')