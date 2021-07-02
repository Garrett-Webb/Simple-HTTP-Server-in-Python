#Garrett Webb

#acknowledgements
#https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
#https://docs.python.org/3/library/http.server.html

import sys
import http.server
import socketserver
import json

class requestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if str(self.path) == '/ping': 
            #if there is something after the ping, this will not trigger

            #send the 200 code
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers() #gotta do this for some reason

            #send the json thing
            response = bytes(json.dumps({'message' : "I'm alive!!"}), 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path).startswith("/ping"):
            #if the string is not exactly /ping but starts with it, not allowed
            self.send_response(405)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = "Method Not Allowed"
            response = bytes(response, 'utf-8')
            self.wfile.write(response)

        elif str(self.path) == '/echo':
            #not a ping, but an echo
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = bytes(json.dumps({'message' : "Get Message Received"}), 'utf-8')
            self.wfile.write(response)

        else:
            #default 500, just for cleaning up loose ends
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        return
    
    def do_POST(self):
        if str(self.path) == '/ping':
            #if there is something after the ping, this will not trigger
            self.send_response(405)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = "Method Not Allowed"
            response = bytes(response, 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path).startswith("/ping"):
            #if starts with ping, but has something after, send 200
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            #get the substring after the /ping/
            response_str = str(self.path).split("/ping/",1)[1]
            response = bytes(json.dumps({'message' : "I'm alive, " + response_str + "!!"}), 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path) == '/echo':
            # not a ping, but an echo
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = bytes("Bad Request", 'utf-8')
            self.wfile.write(response)
        
        elif str(self.path).startswith("/echo?"):
            # echo with a message
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            #get the message from the echo
            response_str = str(self.path).split("/echo?msg=",1)[1]
            response = bytes(json.dumps({'message' : response_str}), 'utf-8')
            self.wfile.write(response)

        else:
            #default 500 code to clean up loose ends
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        return

def run(server_class=http.server.HTTPServer, handler_class=requestHandler, addr='', port=8085):
    # this function initializes and runs the server on the class defined above
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

#call the run function
run()