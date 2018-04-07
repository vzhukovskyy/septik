import sys
import threading

from statistics_collector import StatisticsCollector
from  statistics_logger import StatisticsLogger
import http_server

def main(port):
    sys.stdout.write('Starting HTTP server at port %d ...' % port)
    sys.stdout.flush()

    statistics_collector = StatisticsCollector()
    statistics_collector.start()

    statistics_logger = StatisticsLogger()
    statistics_logger.start()

    print threading.currentThread(),'main',threading.activeCount()

    http_server.run_http_server(port)

    statistics_logger.stop()
    statistics_collector.stop()   

if __name__ == "__main__":
    port = int(sys.argv[1])
    main(port)