import os
import time
import datetime
import sys
import argparse
import signal
import numpy as np
from PIL import Image

import PiCamRunner
import LapsnapWebServer

class Lapsnap():
    def __init__(self, root_image_folder, period, web_port, image_config_file_path):
        self.root_image_folder = root_image_folder
        self.period = period
        self.web_port = web_port
        self.image_config_file_path = image_config_file_path

        self.image_webserver = LapsnapWebServer.LapsnapWebServer(self.web_port)

    def get_day_folder(self, root_folder):
        today = str(datetime.date.today())
        full_path = os.path.join(root_folder, today)
        os.makedirs(full_path, exist_ok=True)
        return full_path

    def save_image(self, image):
        folder = self.get_day_folder(self.root_image_folder)
        name = os.path.join(folder, str(datetime.datetime.now()) + '.jpg')
        img_pil = Image.fromarray(image)
        img_pil.save(name)

    def timelapse_callback(self, image):
        self.save_image(image)
        self.image_webserver.set_last_image(image)

    def run(self):
        picam_runner = PiCamRunner.PiCamRunner(timelapse_period=self.period,
                                               timelapse_callback=self.timelapse_callback,
                                               config_file_path=self.image_config_file_path)

        self.image_webserver.set_picam_runner(picam_runner)
        self.image_webserver.start_image_server()
        picam_runner.run()


def signal_handler():
    raise

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--save_folder', default="./lapsnap_data/", help='path to save images')
    parser.add_argument('--period', default=60, help='period between saved images in seconds')
    parser.add_argument('--web_port', default=3370, help='image viewing website port')
    parser.add_argument('--camera_config', default='~/lapsnap_config.txt', help='path of camera config file')
    args = parser.parse_args()

    signal.signal(signal.SIGTERM, signal_handler)

    lapsnap = Lapsnap(root_image_folder=args.save_folder, period=args.period, web_port=args.web_port, image_config_file_path=args.camera_config)
    lapsnap.run()
