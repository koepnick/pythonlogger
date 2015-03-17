import SocketServer
import SimpleHTTPServer
import json
import pprint
import urlparse
import datetime
from time import strftime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MyTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

class MyTCPServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)
    def do_GET(self):
        try:
            NOW = datetime.datetime.now();
            pprint.pprint(NOW);
            STAMP = strftime( "%H:%M:%S")
            data = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            if( data['type'][0] == 'debug'):
                COLOR = bcolors.OKGREEN
            elif( data['type'][0] == 'error'):
                COLOR = bcolors.FAIL
            elif( data['type'][0] == 'warning'):
                COLOR = bcolors.WARNING
            print bcolors.BOLD + STAMP + bcolors.ENDC + ': ' + bcolors.CYAN + self.client_address[0] + bcolors.ENDC
            print COLOR + data['title'][0] + " : " + data['message'][0] + bcolors.ENDC

        except Exception, e:
            print "Exception wile receiving message: ", e

server = MyTCPServer(('127.0.0.1', 13373), MyTCPServerHandler)
server.serve_forever()