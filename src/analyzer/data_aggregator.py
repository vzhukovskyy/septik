import threading
from datetime import timedelta

from src.db.db import db
from src.common.logger import logger
from src.utils.timeutil import timeutil
from src.analyzer.algorithms import calculate_average


class DataAggregator:
    def start(self):
        self._schedule_next_invocation(3)

    def _schedule_next_invocation(self, timeout):
        now = timeutil.aggregator_now()
        logger.log(logger.CLASS_AGGREGATOR, 'Next aggregation scheduled in {timeout} seconds, at {time}'
                   .format(timeout=timeout, time=now+timedelta(seconds=timeout)))

        self._timer = threading.Timer(timeout, self._timer_func)
        self._timer.start()

    def _timer_func(self):
        self._catch_up_hours_aggregation()

    def _catch_up_hours_aggregation(self):
        aggregation_started_at = timeutil.aggregator_now()
        logger.log(logger.CLASS_AGGREGATOR, 'Hour aggregation started')

        time_from = DataAggregator._get_start_time_of_non_aggregated_data()
        if time_from is None:
            logger.log(logger.CLASS_AGGREGATOR, 'Hour aggregation is up-to-date')
            return

        logger.log(logger.CLASS_AGGREGATOR, 'Starting aggregating from {time}'.format(time=time_from))

        now = timeutil.aggregator_now()
        current_from = time_from
        while True:
            current_to = self._next_period_end(current_from)
            if current_to > now:
                break

            self.aggregate(current_from, current_to)

            current_from = self._next_period_start(current_from)

        logger.log(logger.CLASS_AGGREGATOR, 'Hour aggregation complete')

        aggregation_finished_at = timeutil.aggregator_now()
        if self._start_of_hour(aggregation_started_at) != self._start_of_hour(aggregation_finished_at):
            # the process was started towards the end of hour and it took so long so now there is
            # one more hour to aggregate. Do it right now
            self._schedule_next_invocation(0)
        else:
            now = timeutil.aggregator_now()
            next_hour_start = self._start_of_next_hour(now)
            timeout = next_hour_start-now
            self._schedule_next_invocation(timeout.total_seconds())

    @staticmethod
    def _next_period_end(period_start):
        period_end = period_start + timedelta(hours=1, microseconds=-1)
        return DataAggregator._apply_workaround(period_end)

    @staticmethod
    def _next_period_start(prev_period_start):
        next_period_start = prev_period_start + timedelta(hours=1)
        return DataAggregator._apply_workaround(next_period_start)

    @staticmethod
    def aggregate(time_from, time_to):
        logger.log(logger.CLASS_AGGREGATOR,
                   'processing hour from {time_from} to {time_to}'.format(time_from=time_from, time_to=time_to))
        data = db.query(time_from, time_to)
        av = calculate_average(data)
        if len(av) > 0:
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
                return DataAggregator._start_of_hour(dt)
        else:
            latest = timeutil.parse_db_time(latest[0])
            logger.log(logger.CLASS_AGGREGATOR, 'Latest aggregated hour is {time}'.format(time=latest))
            now = timeutil.aggregator_now()
            if DataAggregator._start_of_hour(latest) == DataAggregator._start_of_hour(now):
                return None
            else:
                return DataAggregator._start_of_next_hour(latest)

    @staticmethod
    def _start_of_hour(time):
        return time.replace(minute=0, second=0, microsecond=0)

    @staticmethod
    def _start_of_next_hour(time):
        dt = time.replace(minute=0, second=0, microsecond=0)+timedelta(hours=1)
        return DataAggregator._apply_workaround(dt)

    @staticmethod
    def _apply_workaround(time):
        return timeutil.make_local(time)
