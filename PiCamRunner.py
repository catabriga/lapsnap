import picamera
import picamera.array
import time

class PiCamRunner():
    def __init__(self, timelapse_period, timelapse_callback, size, rotation, framerate):
        self.timelapse_period = timelapse_period
        self.timelapse_callback = timelapse_callback
        self.size = size
        self.framerate = framerate
        self.rotation = rotation


    def run(self):
        camera = picamera.PiCamera()
        camera.resolution = self.size
        camera.framerate = self.framerate
        camera.rotation = self.rotation

        raw_capture = picamera.array.PiRGBArray(camera, size=camera.resolution)

        # subtract period so that an image is taken as soon as started
        last_time = time.time() - self.timelapse_period

        for frame in camera.capture_continuous(raw_capture, format="rgb", use_video_port=True):

            current_time = time.time()

            image = frame.array

            if(current_time - last_time > self.timelapse_period):
                self.timelapse_callback(image)
                last_time = current_time

            raw_capture.truncate(0)

