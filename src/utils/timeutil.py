import pytz
from datetime import datetime, timedelta
from tzlocal import get_localzone
import dateutil.parser



class TimeUtil:
    def __init__(self):
        self.local_tz = get_localzone()
        self.utc_tz = pytz.timezone('UTC')

    #
    # INTERFACE
    #

    # sensors

    def sensors_now(self):
        return self._timezone_aware_now_in_local()

    # db

    def current_query_date(self):
        return self._timezone_aware_now_in_utc()

    def parse_db_time(self, time):
        return self._parse_tz_unaware_in_local(time)

    def to_db_time(self, time):
        return self._format_tz_aware_to_unaware_in_utc(time)

    # aggregator

    def aggregator_now(self):
        return self._timezone_aware_now_in_local()

    def start_of_hour(self, time):
        dt = time.replace(minute=0, second=0, microsecond=0)
        return self.apply_workaround(dt)

    def start_of_next_hour(self, time):
        dt = time.replace(minute=0, second=0, microsecond=0)+timedelta(hours=1)
        return self.apply_workaround(dt)

    def start_of_day(self, time):
        dt = time.replace(hour=0, minute=0, second=0, microsecond=0)
        return self.apply_workaround(dt)

    def start_of_next_day(self, time):
        dt = time.replace(hour=0, minute=0, second=0, microsecond=0)+timedelta(days=1)
        return self.apply_workaround(dt)

    def apply_workaround(self, dt):
        # when incrementing datetime with timedelta, time zone does not update. This is workaround for this
        return self._timezone_aware_to_local(dt)


    # incoming request from browser

    def parse_incoming_query_date(self, iso):
        dt = self._parse_tz_aware(iso)
        return self._timezone_aware_to_utc(dt)

    # response to browser

    def prepare_sensors_to_json(self, dt):
        dt = self._timezone_aware_to_local(dt)
        return self.to_str(dt)

    def prepare_to_json(self, dt):
        dt = self._timezone_unaware_in_utc_to_local(dt)
        return self.to_str(dt)

    def prepare_array_to_json(self, time_series):
        return [self.prepare_to_json(self._parse_tz_unaware(dt)) for dt in time_series]



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

    def _format_tz_aware_to_unaware_in_utc(self, dt):
        try:
            dt_utc = dt.astimezone(self.utc_tz)
        except:
            pass
        return self.to_str(dt_utc)

    def to_str(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")

    def _timezone_unaware_now_in_utc_str(self):
        return self.to_str(datetime.utcnow())

    def _timezone_unaware_now_in_utc(self):
        return datetime.utcnow()

    def _timezone_aware_now_in_utc(self):
        return datetime.now(self.utc_tz)

    def _timezone_aware_now_in_local(self):
        return datetime.now(self.local_tz)

    def _timezone_unaware_now_in_local(self):
        return datetime.now()

    def _parse_tz_unaware_in_local(self, s):
        dt_naive = dateutil.parser.parse(s)
        dt_tz_aware = self.local_tz.localize(dt_naive)
        return dt_tz_aware

    def _parse_tz_unaware_in_utc(self, s):
        dt_naive = dateutil.parser.parse(s)
        dt_tz_aware = pytz.utc.localize(dt_naive)
        return dt_tz_aware

    def _parse_tz_unaware(self, s):
        return dateutil.parser.parse(s)

    def _parse_tz_aware(self, s):
        return dateutil.parser.parse(s)


timeutil = TimeUtil()
