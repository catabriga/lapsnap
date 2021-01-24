import picamera
import picamera.array
import time
import datetime
import os
import os.path

DEFAULT_CONFIG_PATH = './lapsnap_config.txt'

class PiCamRunner():
    def __init__(self, timelapse_callback):
        self.timelapse_callback = timelapse_callback
        self.camera = picamera.PiCamera()

    def __del__(self):
        self.camera.close()


    def write_default_config_file(self, file_path=DEFAULT_CONFIG_PATH):
        with open(file_path, 'w') as file:
            file.write('resolution = 1640,1232\n')
            file.write('rotation = 0\n')
            file.write('shutter_speed = 0\n')
            file.write('exposure_mode = auto\n')
            file.write('iso = 0\n')
            file.write('exposure_compensation = 0\n')
            file.write('contrast = 0\n')
            file.write('saturation = 0\n')
            file.write('brightness = 50\n')


    def load_configuration(self, file_path=DEFAULT_CONFIG_PATH):
        if not os.path.isfile(file_path):
            self.write_default_config_file(file_path)

        config_dict = {}
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                values = line.split('=')
                try:
                    config_dict[values[0].strip()] = int(values[1])
                    continue
                except:
                    pass    

                try:
                    config_dict[values[0].strip()] = (int(values[1].split(',')[0]), int(values[1].split(',')[1]))
                    continue
                except:
                    pass

                config_dict[values[0].strip()] = values[1].strip()

        self.set_camera_config(config_dict)


    def set_camera_config(self, config_dict):
        for key in config_dict:
            setattr(self.camera, key, config_dict[key])


    def run(self):
        self.load_configuration()
        self.camera.framerate_range = (0.0333, 30)
        self.camera.annotate_foreground = picamera.Color(r=255, g=255, b=255)

        raw_capture = picamera.array.PiRGBArray(self.camera, size=self.camera.resolution)

        while(True):
            start_time = time.time()

            self.camera.annotate_text = str(datetime.datetime.now())
            print('exposure_speed = %d shutter_speed = %d'%(self.camera.exposure_speed, self.camera.shutter_speed))
            self.camera.capture(raw_capture, format='rgb', use_video_port=False)
            image = raw_capture.array
            self.timelapse_callback(image)
            raw_capture.truncate(0)

            end_time = time.time()
            sleep_time = max(self.timelapse_period - (end_time - start_time), 0)
            print('sleep_time = %d'%(sleep_time))
            time.sleep(sleep_time)
            