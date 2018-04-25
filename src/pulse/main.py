import sys
import threading

from src.pulse.data_puller import DataPuller
from src.pulse.data_logger import DataLogger
from src.analyzer.data_aggregator import DataAggregator
import src.pulse.http_server as http_server


def main(port):
    puller = DataPuller()
    puller.start()

    logger = DataLogger()
    logger.start()

    aggregator = DataAggregator()
    aggregator.start()

    http_server.run_http_server(port)

    logger.stop()
    puller.stop()


if __name__ == "__main__":
    port = int(sys.argv[1])
    main(port)