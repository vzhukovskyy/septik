from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from json import JSONDecoder, JSONEncoder
from datetime import datetime
import dateutil.parser
from tzlocal import get_localzone

from latest_data import latestData
from src.db.db import db


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
            self.return_html()
        elif self.path == '/current' or self.path == '/current/':
            self.return_current()

    def do_POST(self):
        json = ""
        if self.headers['Content-Type'] == 'application/json':
            content_length = int(self.headers['Content-Length'])
            json = self.rfile.read(content_length)
        if self.path == '/query' or self.path == '/query/':
            self.return_query(json)

    def return_html(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        f = open('src/pulse/index.html')
        content = f.read()
        self.wfile.write(content.encode('utf-8'))
        f.close()

    def return_current(self):
        data = latestData.get()
        if data is None:
            self.send_response(503)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            print data
            json = JSONEncoder().encode(data)
            self.wfile.write(json.encode('utf-8'))

    def return_query(self, json):
        o = JSONDecoder().decode(json)
        time_from = dateutil.parser.parse(o['from']).astimezone(get_localzone())
        if 'to' in o:
            time_to = dateutil.parser.parse(o['to']).astimezone(get_localzone())
        else:
            time_to = datetime.now()

        records = db.query(time_from, time_to)
        data = db.transpose(records)

        json = JSONEncoder().encode(data)
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
