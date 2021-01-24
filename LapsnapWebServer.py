from PIL import Image
import numpy
from io import BytesIO
import threading
import time
import cherrypy

import random
import string

class LapsnapWebServer:
    def __init__(self, port):
        self.last_image = None
        self.port = port
        self.last_request_time = time.time()

    @cherrypy.expose
    def lastimage(self):
        cherrypy.response.headers['Content-Type'] = 'image/jpg'
        self.last_request_time = time.time()
        img_pil = Image.fromarray(self.last_image)
        mem_file = BytesIO()
        img_pil.save(mem_file, format='jpeg')
        return mem_file.getvalue()

    @cherrypy.expose
    def config(self):
        return """<html>
          <head></head>
          <body>
            <form method="get" action="generate">
              <input type="text" value="8" name="length" />
              <button type="submit">Give it now!</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def generate(self, length=8):
        return ''.join(random.sample(string.hexdigits, int(length)))

    def run_image_server(self):
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})
        cherrypy.config.update({'server.socket_port': self.port})
        cherrypy.quickstart(self)

    def start_image_server(self):
        threading.Thread(target=self.run_image_server, daemon=True).start()

    def set_last_image(self, image):
        self.last_image = image

    def get_last_request_time(self):
        return self.last_request_time

if __name__ == "__main__":

    raspi_server_red = LapsnapWebServer(3370)
    img_red = Image.new('RGB', (60, 30), color = 'red')
    raspi_server_red.set_last_image(numpy.array(img_red))
    raspi_server_red.start_image_server()

    while True:
        time.sleep(1)
