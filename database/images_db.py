from typing import Dict
from aiogram.types import FSInputFile
from PIL import Image
from PIL.Image import Image as ImageType
import logging
import os
import sys
logger = logging.getLogger(__name__)

DEFAULT_STYLE_PATH = "photos/default_style.jpg"
DEFAULT_CONTENT_PATH = "photos/default_content.jpg"
DEFAULT_EPOCH = 300
DEFAULT_RESOLUTION = 256


class Photo():
    def __init__(self,
                 file_id: int | None = None,
                 pil_img: ImageType | None = None,
                 img_path: str | None = None
                 ):
        if img_path is not None:
            path = os.path.join(sys.path[0], os.path.normpath(img_path))
            self.bot_img = FSInputFile(path, filename='content')
            self.pil_img = Image.open(path)
        elif file_id and pil_img:
            self.bot_img = file_id
            self.pil_img = pil_img
        else:
            self.bot_img = None
            self.pil_img = None
            logger.info('Created empty Photo')


class Photos2Transfer():
    def __init__(
        self,
        style: Photo | None = None,
        content: Photo | None = None,
    ):
        self.style = style
        self.content = content


class Parameters():
    def __init__(self,
                 epochs: int = DEFAULT_EPOCH,
                 resolution: int = DEFAULT_RESOLUTION):
        self.epochs = epochs
        self.resolution = resolution
        self.epoch_dict = {
            'epoch100': 100,
            'epoch300': 300,
            'epoch500': 500
        }
        self.resolution_dict = {
            'small': 128,
            'middle': 256,
            'large': 512
        }

    def __str__(self):
        resolution_str = str(self.resolution)
        for key, item in self.resolution_dict.items():
            if item == self.resolution:
                resolution_str = key
                break
        return f'Epochs number is {self.epochs} and ' \
               f'resolution is {resolution_str}.'


class User():
    def __init__(self,
                 user_id: int,
                 params: Parameters | None = Parameters(),
                 photos: Photos2Transfer | None = Photos2Transfer()):
        if not user_id:
            logger.exception('Missing user_id in User class')
            raise Exception('Missing user_id in User class')
        self.user_id = user_id
        self.params = params
        self.photos = photos


# Dictionary where photos and network
# parameters information by user are keeping
users: Dict[int, User] = {}
