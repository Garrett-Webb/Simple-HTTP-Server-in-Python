#https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
#https://docs.python.org/3/library/http.server.html

import sys
import http.server
import socketserver
import json

class requestHandler(http.server.SimpleHTTPRequestHandler):
    
    def send_response_code(self, response_code):
        self.send_response(response_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    
    def do_GET(self):
        if str(self.path) == '/ping': #if there is something after the ping, this will not trigger
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = bytes(json.dumps({'message' : "I'm alive!!"}), 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path).startswith("/ping"):
            self.send_response(405)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = "Method Not Allowed"
            response = bytes(response, 'utf-8')
            self.wfile.write(response)

        elif str(self.path) == '/echo':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = bytes(json.dumps({'message' : "Get Message Received"}), 'utf-8')
            self.wfile.write(response)

        else:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        return
    
    def do_POST(self):
        if str(self.path) == '/ping':
            self.send_response(405)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = "Method Not Allowed"
            response = bytes(response, 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path).startswith("/ping"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response_str = str(self.path).split("/ping/",1)[1]
            response = bytes(json.dumps({'message' : "I'm alive, " + response_str + "!!"}), 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path) == '/echo':
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = bytes("Bad Request", 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path).startswith("/echo?"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response_str = str(self.path).split("/echo?msg=",1)[1]
            response = json.dumps({'message' : "I'm alive!!"})
            response = bytes(json.dumps({'message' : response_str}), 'utf-8')
            self.wfile.write(response)

        else:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        return

def run(server_class=http.server.HTTPServer, handler_class=requestHandler, addr='', port=8085):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()