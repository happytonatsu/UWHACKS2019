import datetime
import json

def json_serial(obj):

    obj  = obj.__dict__
    obj.pop('_sa_instance_state', None)

    for k, v in obj.items():
        if isinstance(v, (datetime.datetime, datetime.date)):
            obj[k] = v.isoformat()

    return json.dumps(obj)
