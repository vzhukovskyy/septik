import threading
from datetime import timedelta

from src.db.db import db
from src.common.logger import logger
from src.utils.timeutil import timeutil
from src.analyzer.algorithms import calculate_average


class HourlyAggregator:
    def catch_up_aggregation(self):
        logger.log(logger.CLASS_AGGREGATOR, 'Hour aggregation started')

        time_from = self._get_start_time_of_non_aggregated_data()
        if time_from is None:
            logger.log(logger.CLASS_AGGREGATOR, 'Hour aggregation is up-to-date')
            return

        logger.log(logger.CLASS_AGGREGATOR, 'Starting hourly aggregation from {time}'.format(time=time_from))

        now = timeutil.aggregator_now()
        current_from = time_from
        while True:
            current_to = self._next_hour_end(current_from)
            if current_to > now:
                break

            self.aggregate(current_from, current_to)

            current_from = self._next_hour_start(current_from)

        logger.log(logger.CLASS_AGGREGATOR, 'Hourly aggregation complete')

    @staticmethod
    def _next_hour_end(hour_start):
        hour_end = hour_start + timedelta(hours=1, microseconds=-1)
        return timeutil.apply_workaround(hour_end)

    @staticmethod
    def _next_hour_start(prev_hour_start):
        next_hour_start = prev_hour_start + timedelta(hours=1)
        return timeutil.apply_workaround(next_hour_start)

    @staticmethod
    def aggregate(time_from, time_to):
        logger.log(logger.CLASS_AGGREGATOR,
                   'processing hour from {time_from} to {time_to}'.format(time_from=time_from, time_to=time_to))
        data = db.select_between('sensors', time_from, time_to)
        av = calculate_average(data)
        if len(av) > 0:
            av[0] = time_from.replace(minute=30)
            db.insert('hours', av)

    @staticmethod
    def _get_start_time_of_non_aggregated_data():
        latest = db.select_latest('hours')
        if latest is None:
            logger.log(logger.CLASS_AGGREGATOR, 'No data in hours table')
            earliest = db.select_earliest('sensors')
            if earliest is None:
                logger.log(logger.CLASS_AGGREGATOR, 'No data in sensors table')
                return None
            else:
                logger.log(logger.CLASS_AGGREGATOR, 'Earliest record in sensors table dated {time}'.format(time=earliest[0]))
                dt = timeutil.parse_db_time(earliest[0])
                return timeutil.start_of_hour(dt)
        else:
            latest = timeutil.parse_db_time(latest[0])
            logger.log(logger.CLASS_AGGREGATOR, 'Latest aggregated hour is {time}'.format(time=latest))
            now = timeutil.aggregator_now()
            if timeutil.start_of_hour(latest) == timeutil.start_of_hour(now):
                return None
            else:
                return timeutil.start_of_next_hour(latest)



