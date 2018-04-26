import threading
from datetime import timedelta

from src.db.db import db
from src.common.logger import logger
from src.utils.timeutil import timeutil
from src.analyzer.algorithms import calculate_average


class DailyAggregator:
    def catch_up_aggregation(self):
        logger.log(logger.CLASS_AGGREGATOR, 'Daily aggregation started')

        time_from = self._get_start_time_of_non_aggregated_data()
        if time_from is None:
            logger.log(logger.CLASS_AGGREGATOR, 'Daily aggregation is up-to-date')
            return

        logger.log(logger.CLASS_AGGREGATOR, 'Starting daily aggregation from {time}'.format(time=time_from))

        now = timeutil.aggregator_now()
        current_from = time_from
        while True:
            current_to = self._day_end(current_from)
            if current_to > now:
                break

            self.aggregate(current_from, current_to)

            current_from = self._next_day_start(current_from)

        logger.log(logger.CLASS_AGGREGATOR, 'Daily aggregation complete')

    @staticmethod
    def _day_end(day_start):
        day_end = day_start + timedelta(days=1, microseconds=-1)
        return timeutil.apply_workaround(day_end)

    @staticmethod
    def _next_day_start(prev_day_start):
        next_day_start = prev_day_start + timedelta(days=1)
        return timeutil.apply_workaround(next_day_start)

    @staticmethod
    def aggregate(time_from, time_to):
        logger.log(logger.CLASS_AGGREGATOR,
                   'processing day from {time_from} to {time_to}'.format(time_from=time_from, time_to=time_to))
        data = db.select_between('hours', time_from, time_to)
        av = calculate_average(data)
        if len(av) > 0:
            av[0] = time_from.replace(hour=12)
            db.insert('days', av)

    @staticmethod
    def _get_start_time_of_non_aggregated_data():
        latest = db.select_latest('days')
        if latest is None:
            logger.log(logger.CLASS_AGGREGATOR, 'No data in days table')
            earliest = db.select_earliest('hours')
            if earliest is None:
                logger.log(logger.CLASS_AGGREGATOR, 'No data in hours table')
                return None
            else:
                logger.log(logger.CLASS_AGGREGATOR, 'Earliest record in hours table dated {time}'.format(time=earliest[0]))
                dt = timeutil.parse_db_time(earliest[0])
                return timeutil.start_of_day(dt)
        else:
            latest = timeutil.parse_db_time(latest[0])
            logger.log(logger.CLASS_AGGREGATOR, 'Latest aggregated day is {time}'.format(time=latest))
            now = timeutil.aggregator_now()
            if timeutil.start_of_day(latest) == timeutil.start_of_day(now):
                return None
            else:
                return timeutil.start_of_next_day(latest)


