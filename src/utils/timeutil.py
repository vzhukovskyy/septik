import pytz
from datetime import datetime
from tzlocal import get_localzone
import dateutil.parser


class TimeUtil:
    def __init__(self):
        self.local_tz = get_localzone()
        self.utc_tz = pytz.timezone('UTC')

    #
    # INTERFACE
    #

    # request is in ISO format, i.e. timezone aware. 
    # Just for sanity convert to UTC.
    def parse_incoming_query_date(self, iso):
        dt = self._parse_tz_aware(iso)
        return self._timezone_aware_to_utc(dt)

    # when no end date specified in JSON query,
    # use current UTC time
    def current_query_date(self):
        return self._timezone_unaware_now_in_utc()

    # string used in latest sensor data
    def sensors_now(self):
        return self._timezone_unaware_now_in_utc()

    def prepare_sensors_to_json(self, dt):
        dt = self._timezone_unaware_in_utc_to_local(dt)
        return self.to_str(dt)

    # used to convert time from DB to JSON response
    def prepare_to_json(self, dt):
        dt = self._timezone_unaware_in_utc_to_local(dt)
        return self.to_str(dt)

    # used to convert time from DB to JSON response
    def prepare_array_to_json(self, time_series):
        return [self.prepare_to_json(self._parse_tz_unaware(dt)) for dt in time_series]

    def parse_db_time(self, time):
        return self._parse_tz_unaware_in_utc(time)
    #
    # IMPLEMENTATION
    #

    def _timezone_unaware_in_utc_to_local(self, dt):
        dt_tz_aware = pytz.utc.localize(dt)
        return dt_tz_aware.astimezone(self.local_tz)

    def _timezone_aware_to_utc(self, dt):
        return dt.astimezone(self.utc_tz)

    def _timezone_aware_to_local(self, dt):
        return dt.astimezone(self.local_tz)

    def to_str(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")

    def _timezone_unaware_now_in_utc_str(self):
        return self.to_str(datetime.utcnow())

    def _timezone_unaware_now_in_utc(self):
        return datetime.utcnow()

    def _timezone_unaware_now_in_local(self):
        return datetime.now()

    def _parse_tz_unaware_in_local(self, s):
        return dateutil.parser.parse(s).astimezone(self.local_tz)

    def _parse_tz_unaware_in_utc(self, s):
        dt_naive = dateutil.parser.parse(s)
        dt_tz_aware = pytz.utc.localize(dt_naive)
        return dt_tz_aware

    def _parse_tz_unaware(self, s):
        return dateutil.parser.parse(s)

    def _parse_tz_aware(self, s):
        return dateutil.parser.parse(s)


timeutil = TimeUtil()
