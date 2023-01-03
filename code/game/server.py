import http.server
import socketserver
from os import path

my_host_name = 'localhost'
my_port = 8888
my_html_folder_path = 'C:\\Users\\Acer\\PycharmProjects\\e16-4yp-Enhancing-Video-Game-Experience-With-Brain-Computer-Interface\\code\\game\\'

my_home_page_file_path = 'mini_game.html'


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

      def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', path.getsize(self.getPath()))
        self.end_headers()

      def getPath(self):
            if self.path == '/':
                  content_path = path.join(
                        my_html_folder_path, my_home_page_file_path)
            else:
                  content_path = path.join(my_html_folder_path, str(self.path).split('?')[0][1:])
            print("content_path",content_path)
            
            return content_path

      def getContent(self, content_path):
            with open(content_path, mode='r', encoding='utf-8') as f:
                  content = f.read()
            return bytes(content, 'utf-8')

      def do_GET(self):
            self._set_headers()
            self.wfile.write(self.getContent(self.getPath()))


my_handler = MyHttpRequestHandler

with socketserver.TCPServer(("", my_port), my_handler) as httpd:
    print("Http Server Serving at port", my_port)
    httpd.serve_forever()
