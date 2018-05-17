from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import os


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("Works")

    def do_POST(self):

        hostname = str(self.client_address[0])
        filename = "hackday_logs/"+hostname+".log"

        length = int(self.headers.getheader('content-length'))
        field_data = self.rfile.read(length)
        fields = urlparse.parse_qs(field_data)

    	if not os.path.isfile(filename):
    		with open(filename, 'w') as writefile:
            writefile.write("index;")
            writefile.write("time;")
            writefile.write("cpu-0-idle;cpu-1-idle;")
            writefile.write("free-mem;")
            writefile.write("rxpck/s;txpck/s;")
            writefile.write("\n")

        with open(filename, 'a') as appendfile:
            appendfile.write(fields.get("index")[0]+";")
            appendfile.write(fields.get("time")[0]+";")
            appendfile.write(fields.get("cpu-0-idle")[0]+";")
            appendfile.write(fields.get("cpu-1-idle")[0]+";")
            appendfile.write(fields.get("free-mem")[0]+";")
            appendfile.write(fields.get("rxpck/s")[0]+";")
            appendfile.write(fields.get("txpck/s")[0]+";")        
            appendfile.write("\n")
        print "POST received."
        

def run(server_class=HTTPServer, handler_class=Server, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()