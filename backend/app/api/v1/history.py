from flask import Blueprint, request
from app.utils import send_result, send_error, notification
from app.extensions import client
from flask_jwt_extended import (
    jwt_required)

api = Blueprint('history', __name__)


@api.route('/get_all_page_search', methods=['GET'])
@jwt_required
def get_all_page_search():
    page_size = request.args.get('page_size', '25')
    page_number = request.args.get('page_number', '0')
    skips = int(page_size) * int(page_number)
    '''Give list after filtering'''

    users = client.db.history.find().skip(skips).limit(int(page_size)).sort('_id', -1)
    '''end list'''
    list_user = list(users)
    totals = client.db.history.find().count()
    data = {
        'totals': totals,
        'results': list_user
    }
    return send_result(data=data)


@api.route('/get_by_id', methods=['GET'])
@jwt_required
def get_by_id():
    history_id = request.args.get('history_id')
    history = client.db.history.find_one({'_id': history_id})
    if not history:
        return send_error(message="Không tìm thấy bản ghi")
    data = {
        'results': history
    }
    return send_result(data=data)
