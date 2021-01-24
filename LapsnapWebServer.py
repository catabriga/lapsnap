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
        return """
    <html>
        <head></head>
        <body>
            <a href="https://picamera.readthedocs.io/en/release-1.13/api_camera.html" target="_blank">camera api<a/>

            <form method="get" action="save_config">
                <div>
                  <label for="resolution">resolution: </label>
                  <input type="text" value="1640,1232" name="resolution" />
                </div>

                <div>
                  <label for="rotation">rotation: </label>
                  <input type="text" value="0" name="rotation" />
                </div>

                <div>
                  <label for="shutter_speed">shutter_speed: </label>
                  <input type="text" value="0" name="shutter_speed" />
                </div>

                <div>
                  <label for="exposure_mode">exposure_mode: </label>
                  <input type="text" value="auto" name="exposure_mode" />
                </div>

                <div>
                  <label for="iso">iso: </label>
                  <input type="text" value="0" name="iso" />
                </div>

                <div>
                  <label for="exposure_compensation">exposure_compensation: </label>
                  <input type="text" value="0" name="exposure_compensation" />
                </div>

                <div>
                  <label for="contrast">contrast: </label>
                  <input type="text" value="0" name="contrast" />
                </div>

                <div>
                  <label for="saturation">saturation: </label>
                  <input type="text" value="0" name="saturation" />
                </div>

                <div>
                  <label for="brightness">brightness: </label>
                  <input type="text" value="50" name="brightness" />
                </div>
                <button type="submit">save</button>
            </form>
        </body>
    </html>
    """

    @cherrypy.expose
    def save_config(self, resolution, rotation, shutter_speed, exposure_mode, iso, exposure_compensation, contrast, saturation, brightness):
        return 'configuration saved'

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
