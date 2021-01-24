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
            camera.framerate_range = (0.0333, 30)
            camera.shutter_speed = 3000000
            camera.exposure_mode = 'night'
            camera.iso = 800
            camera.exposure_compensation = 25
            camera.contrast = 0
            camera.saturation = 0
            camera.brightness = 50

            raw_capture = picamera.array.PiRGBArray(camera, size=camera.resolution)

            last_time = time.time()

            while(True):
                current_time = time.time()

                camera.annotate_text = str(datetime.datetime.now())
                print('exposure_speed = %d shutter_speed = %d'%(camera.exposure_speed, camera.shutter_speed))
                camera.capture(raw_capture, format='rgb', use_video_port=False)
                print('exposure_speed = %d shutter_speed = %d'%(camera.exposure_speed, camera.shutter_speed))
                image = raw_capture.array
                self.timelapse_callback(image)
                raw_capture.truncate(0)

                sleep_time = max(self.timelapse_period - (current_time - last_time), 0)
                last_time = current_time
                print('current_time = %d last_time = %d dt = %d sleep_time = %d'%(current_time, last_time, current_time-last_time), sleep_time)
                time.sleep(sleep_time)