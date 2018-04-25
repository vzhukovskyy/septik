import thread
from datetime import timedelta

from src.db.db import db
from src.common.logger import logger
from src.utils.timeutil import timeutil
from src.analyzer.algorithms import calculate_average


class DataAggregator:
    def start(self):
        thread.start_new_thread(self.catch_up_hours_aggregation, (),)

    def queue_next_invocation(self):
        pass #TODO

    def schedule_next_invocation(self):
        pass #TODO

    def catch_up_hours_aggregation(self):
        time_from = self._get_from()
        if time_from is None:
            logger.log(logger.CLASS_AGGREGATOR, 'Hour aggregation is up-to-date')
            return

        time_from = self._start_of_next_hour(time_from)
        logger.log(logger.CLASS_AGGREGATOR, 'Starting aggregating from {time}'.format(time=time_from))

        now = timeutil.aggregator_now()
        nhours = int((now-time_from).total_seconds() // 3600)
        logger.log(logger.CLASS_AGGREGATOR, 'total hours to aggregate: {hours}'.format(hours=nhours))
        current_from = time_from
        while True:
            current_to = current_from + timedelta(hours=1, microseconds=-1)
            #workaround against time zone not changing when incrementing hours
            current_to = timeutil.make_local(current_to)
            if current_to > now:
                break

            self.aggregate(current_from, current_to)

            current_from += timedelta(hours=1)
            # workaround against time zone not changing when incrementing hours
            current_from = timeutil.make_local(current_from)

        logger.log(logger.CLASS_AGGREGATOR, 'Hour aggregation complete')

    def aggregate(self, time_from, time_to):
        logger.log(logger.CLASS_AGGREGATOR,
                   'processing hour from {time_from} to {time_to}'.format(time_from=time_from, time_to=time_to))
        data = db.query(time_from, time_to)
        av = calculate_average(data)
        if len(av) > 0:
            db.insert('hours', av)

    def _get_from(self):
        latest = db.select_latest('hours')
        if latest is None:
            logger.log(logger.CLASS_AGGREGATOR, 'No data in hours table')
            earliest = db.select_earliest('sensors')
            if earliest is None:
                logger.log(logger.CLASS_AGGREGATOR, 'No data in sensors table')
                return None
            else:
                logger.log(logger.CLASS_AGGREGATOR, 'Earliest record in sensors table dated {time}'.format(time=earliest[0]))
                return timeutil.parse_db_time(earliest[0])
        else:
            latest = timeutil.parse_db_time(latest[0])
            logger.log(logger.CLASS_AGGREGATOR, 'Latest aggregated hour is {time}'.format(time=latest))
            now = timeutil.aggregator_now()
            dt = now-latest
            logger.log(logger.CLASS_AGGREGATOR, 'Diff between now and latest {delta}'.format(delta=dt))
            if dt.total_seconds() < 3600 and latest.hour == now.hour:
                return None
            else:
                return latest

    def _start_of_next_hour(self, time):
        return time.replace(minute=0, second=0, microsecond=0)+timedelta(hours=1)