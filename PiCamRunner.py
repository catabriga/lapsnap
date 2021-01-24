import picamera
import picamera.array
import time
import datetime

class PiCamRunner():
    def __init__(self, timelapse_period, timelapse_callback, size, rotation, framerate):
        self.timelapse_period = timelapse_period
        self.timelapse_callback = timelapse_callback
        self.size = size
        self.framerate = framerate
        self.rotation = rotation


    def run(self):
        with picamera.PiCamera() as camera:
            camera.resolution = self.size
            camera.rotation = self.rotation
            camera.shutter_speed = 6000000
            camera.exposure_mode = 'night'
            camera.iso = 800
            camera.exposure_compensation = 25
            camera.contrast = -50
            camera.saturation = 0
            camera.brightness = 50

            raw_capture = picamera.array.PiRGBArray(camera, size=camera.resolution)

            last_time = time.time()

            while(True):
                camera.annotate_text = str(datetime.datetime.now())
                camera.capture(raw_capture, format="rgb", use_video_port=False)
                image = raw_capture.array
                self.timelapse_callback(image)
                raw_capture.truncate(0)

                current_time = time.time()
                sleep_time = max(self.timelapse_period - (current_time - last_time), 0)
                time.sleep(sleep_time)