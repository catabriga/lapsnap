import os
import time
import datetime
import sys
import argparse
import signal
import numpy as np
from PIL import Image

import PiCamRunner

class Lapsnap():
    def __init__(self, root_image_folder, period, size, rotation, framerate):
        self.root_image_folder = root_image_folder
        self.period = period
        self.size = tuple(size)
        self.rotation = rotation
        self.framerate = framerate

    def get_day_folder(self, root_folder):
        today = str(datetime.date.today())
        full_path = os.path.join(root_folder, today)
        os.makedirs(full_path, exist_ok=True)
        return full_path

    def save_image(self, image):
        folder = self.get_day_folder(self.root_image_folder)
        name = os.path.join(folder, str(datetime.datetime.now()) + '.jpg')
        img_pil = Image.fromarray(image)
        image.save(name)

    def timelapse_callback(self, image):
        self.save_image(image)

    def run(self):
        picam_detector = PiCamRunner.PiCamRunner(timelapse_period=self.period,
                                                 timelapse_callback=self.timelapse_callback,
                                                 size=self.size,
                                                 rotation=self.rotation,
                                                 framerate=self.framerate)

        picam_detector.run()


def signal_handler():
    raise

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--save_folder', default="./lapsnap_data/", help='path to save images')
    parser.add_argument('--period', default=60, help='period between saved images in seconds')
    parser.add_argument('--size', nargs=2, default=[640,480], help='image resolution')
    parser.add_argument('--rotation', default=0, help='image rotation')
    parser.add_argument('--framerate', default=10, help='capture framerate')
    args = parser.parse_args()

    signal.signal(signal.SIGTERM, signal_handler)

    lapsnap = Lapsnap(root_image_folder=args.save_folder, period=args.period, size=args.size,
                      rotation=args.rotation, framerate=args.framerate)
    lapsnap.run()
