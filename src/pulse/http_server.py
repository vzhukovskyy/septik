from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from json import JSONDecoder, JSONEncoder
from datetime import datetime
import dateutil.parser
from tzlocal import get_localzone

import utils
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
        elif self.path == '/query' or self.path == '/query/':
            self.return_query(None)

    def do_POST(self):
        json = ""
        if self.headers['Content-Type'] == 'application/json':
            content_length = int(self.headers['Content-Length'])
            json = self.rfile.read(content_length)

        print "Request handler", self.path
        print "JSON"
        print json

        if self.path == '/query' or self.path == '/query/':
            self.return_query(json)

    def return_html(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        f = open('src/pulse/index.html')
        content = f.read()
        #print content
        print('Returned index.html')
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
        print 'Request arrived', datetime.now()
        o = JSONDecoder().decode(json)
        time_from = dateutil.parser.parse(o['from'])
        print 'Request string', o['from']
        print 'UTC',time_from
        print 'As local',time_from.astimezone(get_localzone())
        time_from = time_from.astimezone(get_localzone())
        if 'to' in o:
            time_to = dateutil.parser.parse(o['to'])
        else:
            time_to = datetime.now()
        # time_from = utils.parse_datetime("2018-01-01 00:00:00")
        # time_to = utils.parse_datetime("2018-01-03 00:00:00")
        print 'From',time_from,'To',time_to

        records = db.query(time_from, time_to)

        series = [[r[col] for r in records] for col in range(len(records[0]))]
        columns = db.columns()
        print series
        print columns
        data = {columns[i]:series[i] for i in range(len(columns))}
        json = JSONEncoder().encode(data)

        json = json.encode('utf-8')
        print 'response length',len(json)
        self.send_response(200)
        # It takes 30 seconds for Postman aload 8Mb of application/json
        # browser needs 1 minutes for this
        # application/text is shown in 5 seconds in browser
        # and 30 seconds in Postman
        # TODO: measure if loaded by javascript
        self.send_header('Content-Type', 'application/json')
        #self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(json))
        self.end_headers()
        print 'JSON prepared',datetime.now()
        self.wfile.write(json)
        print 'JSON sent',datetime.now()


def run_http_server(port):
    http_server = HTTPServer(('', port), RESTRequestHandler)
    print(' done.')
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    print('Stopping HTTP server')
    http_server.server_close()

