from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from latest_data import latest_data, latest_filtered_data
from src.db.db import db
from src.utils.timeutil import timeutil
from src.analyzer.filter import data_filter
from json_utils import toJSON, fromJSON


class RESTRequestHandler(BaseHTTPRequestHandler):
    #hack: overridden to avoid extreme sluggishness caused by FQDN lookup
    #https://stackoverflow.com/a/5273870
    def address_string(self):
        host, port = self.client_address[:2]
        #return socket.getfqdn(host)
        return host

    def do_GET(self):
        print("Request handler", self.path)
        if self.path == '/':
            self.return_html('src/pulse/realtime.html')
        elif self.path == '/threedays.html':
            self.return_html('src/pulse/threedays.html')
        elif self.path == '/current' or self.path == '/current/':
            self.return_current()

    def do_POST(self):
        json = ""
        if self.headers['Content-Type'] == 'application/json':
            content_length = int(self.headers['Content-Length'])
            json = self.rfile.read(content_length)
        if self.path == '/query' or self.path == '/query/':
            self.return_query(json)

    def return_html(self, path):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        f = open(path)
        content = f.read()
        self.wfile.write(content.encode('utf-8'))
        f.close()

    def return_current(self):
        raw_data = latest_data.get()
        filtered_data = latest_filtered_data.get()
        if raw_data is None:
            self.send_response(503)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            data = dict(raw=raw_data, filtered=filtered_data)

            json = toJSON(data)
            self.wfile.write(json.encode('utf-8'))

    def return_query(self, json):
        o = fromJSON(json)
        time_from = timeutil.parse_incoming_query_date(o['from'])
        if 'to' in o:
            time_to = timeutil.parse_incoming_query_date(o['to'])
        else:
            time_to = timeutil.current_query_date()

        records = db.query(time_from, time_to)
        raw_data = db.transpose(records)
        filtered_data, kalman = data_filter.reverse_filter_series(raw_data, latest_filtered_data.get())
        data = dict(raw=raw_data, filtered=filtered_data)

        json = toJSON(data)
        json = json.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json))
        self.end_headers()
        self.wfile.write(json)


def run_http_server(port):
    http_server = HTTPServer(('', port), RESTRequestHandler)
    print(' done.')
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    print('Stopping HTTP server')
    http_server.server_close()
