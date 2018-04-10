
def jsonify(adict):
    s = '{'
    first = True
    for key,value in adict.items():
        if first:
            first = False
        else:
            s += ','

        if isinstance(value, str):
            value = '"'+value+'"'

        s += '"'+key+'"' + ':' + str(value)
    s += '}'
    return s