from json import JSONDecoder, JSONEncoder, dumps
from datetime import datetime


def fromJSON(json):
    return JSONDecoder().decode(json)

def toJSON(data):
    #return JSONEncoder().encode(data)
    return dumps(data, default=_converter)


def _converter(o):
    if isinstance(o, datetime):
        return o.__str__()
