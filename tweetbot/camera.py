from datetime import datetime
from os import makedirs
from os.path import isdir, join
from time import sleep

import picamera as pc


def take_photo(dest_folder='Photos'):
    # TODO Add docstring
    if not isdir(dest_folder):
        makedirs(dest_folder)

    camera = pc.PiCamera(resolution=(1024, 768))

    camera.annotate_background = pc.Color('black')
    camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M')

    camera.start_preview()
    sleep(5)

    output_location = join(
        dest_folder, datetime.now().strftime('%Y-%m-%d %H%M') + '.png'
    )

    camera.capture(output_location)
    camera.stop_preview()

    return output_location


if __name__ == '__main__':
    take_photo()
