from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from utils import jsonify
from latest_data import latestData


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
        elif self.path == '/stat' or self.path == '/stat/':
            self.return_json()
    
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

    def return_json(self):
        data = latestData.get()
        if data is None:
            self.send_response(503)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()   
            json = jsonify(data)
            self.wfile.write(json.encode('utf-8'))


def run_http_server(port):
    http_server = HTTPServer(('', port), RESTRequestHandler)
    print(' done.')
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass
    print('Stopping HTTP server')
    http_server.server_close()

