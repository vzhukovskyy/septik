from tzlocal import get_localzone


_local_tz = get_localzone()


def _datetime_utc_to_local(dt):
    return dt.astimezone(_local_tz)

def _list_utc_to_local(list):
    return [dt.astimezone(_local_tz) for dt in list]
