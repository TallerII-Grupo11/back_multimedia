from bson import json_util
import json
from fastapi.encoders import jsonable_encoder

def get_list(list_data):
    data = []
    for x in list_data:
        data_json = jsonable_encoder(x)
        data_json["id"] = data_json["_id"]
        del data_json["_id"]
        data.append(data_json)
    return data


def get_data(data):
    data_json = json.loads(json_util.dumps(data))
    data_json["id"] = data_json["_id"]
    del data_json["_id"]
    return data_json

