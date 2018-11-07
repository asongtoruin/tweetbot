from datetime import datetime
from os import mkdir
from os.path import isdir, join
from time import sleep

from picamera import PiCamera


DESTINATION_FOLDER = 'Photos'


def take_photo():
    # TODO Add docstring
    if not isdir(DESTINATION_FOLDER):
        mkdir(DESTINATION_FOLDER)

    camera = PiCamera()

    camera.start_preview()
    sleep(5)

    output_location = join(
        DESTINATION_FOLDER, datetime.now().strftime('%Y-%m-%d %H%M%S')
    )

    camera.capture(output_location)
    camera.stop_preview()

    return output_location
