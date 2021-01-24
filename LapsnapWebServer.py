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
        self.picam_runner = None

    def set_picam_runner(self, picam_runner):
        self.picam_runner = picam_runner        

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
        config_dict = self.picam_runner.read_configuration()

        html_start = """<html><head></head><body>
            <a href="https://picamera.readthedocs.io/en/release-1.13/api_camera.html" target="_blank">camera api<a/>
            <form method="get" action="save_config">"""
        html_end = """<button type="submit">save</button></form><form method="get" action="reset_config"><button type="submit">reset to default</button></form></body></html>"""

        html_divs = ""
        for key in config_dict:
            html_divs += '<div><label for="%s">%s: </label><input type="text" value="%s" name="resolution" /></div>'%(key,key,config_dict[key])

        return html_start + html_divs + html_end

    @cherrypy.expose
    def save_config(self, resolution, rotation, shutter_speed, exposure_mode, iso, exposure_compensation, contrast, saturation, brightness):
        return 'configuration saved'

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
