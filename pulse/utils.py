def jsonify(adict):
    s = '{'
    first = True
    for key,value in adict.iteritems():
        if first:
            first = False
        else:
            s += ',' 
        s += '"'+key+'"' + ':' + str(value)
    s += '}'
    return s