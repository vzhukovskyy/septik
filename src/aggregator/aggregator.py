import threading
from datetime import timedelta

from src.common.logger import logger
from src.utils.timeutil import timeutil
from src.aggregator.hourly_aggregator import HourlyAggregator
from src.aggregator.daily_aggregator import DailyAggregator


class Aggregator:
    def __init__(self):
        self._timer = None
        self._lock = threading.Lock()
        self.hourly_aggregator = HourlyAggregator()
        self.daily_aggregator = DailyAggregator()

    def start(self):
        self._schedule_next_call(3)

    def stop(self):
        self._cancel_next_call()

    def _schedule_next_call(self, timeout):
        if timeout < 0:
            timeout = 0

        with self._lock:
            now = timeutil.aggregator_now()
            logger.log(logger.CLASS_AGGREGATOR, 'Next aggregation scheduled in {timeout} seconds, at {time}'
                       .format(timeout=timeout, time=now+timedelta(seconds=timeout)))

            self._timer = threading.Timer(timeout, self._timer_func)
            self._timer.start()

    def _cancel_next_call(self):
        with self._lock:
            self._timer.cancel()

    def _timer_func(self):
        aggregation_started_at = timeutil.aggregator_now()

        self.hourly_aggregator.catch_up_aggregation()
        self.daily_aggregator.catch_up_aggregation()

        next_hour_start = timeutil.start_of_next_hour(aggregation_started_at)
        timeout = next_hour_start-aggregation_started_at
        self._schedule_next_call(timeout.total_seconds())
