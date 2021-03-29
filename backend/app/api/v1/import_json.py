from flask import Blueprint, json
from app.extensions import client
from flask_jwt_extended import (
    jwt_required
)
from bson import ObjectId
api = Blueprint('import_json', __name__)


@api.route('/read_file_json', methods=['GET'])
@jwt_required
def read_file_json():
    try:
        with open('/home/ducdv10/Documents/do_an/backend/ok.json', encoding="utf8") as f:
            list_data = json.load(f)
    except Exception as ex:
        print(ex)

    for data in list_data:
        if data['types'][0] == 'hospital':
            if not list(client.db.hospital.find({'name': data['name']})):
                data["location"] = {"lat": data["geometry"]["location"]["lat"],
                                    "lng": data["geometry"]["location"]["lng"]}
                data["_id"] = str(ObjectId())
                client.db.hospital.insert(data)
        elif data['types'][0] == 'fire_station':
            if not list(client.db.fire_station.find({'name': data['name']})):
                data["location"] = {"lat": data["geometry"]["location"]["lat"],
                                    "lng": data["geometry"]["location"]["lng"]}
                data["_id"] = str(ObjectId())
                client.db.fire_station.insert(data)
        elif data['types'][0] == 'police':
            if not list(client.db.police.find({'name': data['name']})):
                data["location"] = {"lat": data["geometry"]["location"]["lat"],
                                    "lng": data["geometry"]["location"]["lng"]}
                data["_id"] = str(ObjectId())
                client.db.police.insert(data)
        else:
            if not list(client.db.apartment.find({'name':data['name']})):
                data["location"] = {"lat": data["geometry"]["location"]["lat"],
                                    "lng": data["geometry"]["location"]["lng"]}
                data["_id"] = str(ObjectId())
                client.db.apartment.insert(data)
