from datetime import datetime
from os import makedirs, remove
from os.path import isdir, join
from time import sleep

import picamera as pc


class EasyCamera:
    def __init__(self):
        self.camera = pc.PiCamera(resolution=(1200, 800))
        self.camera.annotate_background = pc.Color('black')
        self.camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M')

    @staticmethod
    def output_location(folder_name, file_ext):
        if not isdir(folder_name):
            makedirs(folder_name)

        return join(
            folder_name, datetime.now().strftime('%Y-%m-%d %H%M') + file_ext
        )

    def take_photo(self, dest_folder='Photos'):
        # TODO Add docstring
        out = self.output_location(dest_folder, '.png')

        self.camera.start_preview()
        sleep(5)
        self.camera.capture(out)
        self.camera.stop_preview()

        return out

    def record_video(self, dest_folder='Videos', duration_secs=10):
        import subprocess

        out = self.output_location(dest_folder, '.h264')
        mp4_out = out.replace('.h264', '.mp4')
        self.camera.start_preview()
        self.camera.start_recording(out)
        sleep(duration_secs)
        self.camera.stop_recording()
        self.camera.stop_preview()

        # Use gpac to convert from .h264 to .mp4
        # install with
        process = subprocess.Popen(
            ['MP4Box', '-add', out, mp4_out], stdout=subprocess.PIPE
        )

        stdout = process.communicate()

        print(stdout)
        remove(out)

        return mp4_out


if __name__ == '__main__':
    cam = EasyCamera()
    cam.take_photo()
    cam.record_video()
