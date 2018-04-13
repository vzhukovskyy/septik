import sys
import threading

from data_puller import DataPuller
from data_logger import DataLogger
import http_server


def main(port):
    sys.stdout.write('Starting HTTP server at port %d ...' % port)
    sys.stdout.flush()

    puller = DataPuller()
    puller.start()

    logger = DataLogger()
    logger.start()

    print(threading.currentThread(),'main',threading.activeCount())

    http_server.run_http_server(port)

    logger.stop()
    puller.stop()


if __name__ == "__main__":
    port = int(sys.argv[1])
    main(port)