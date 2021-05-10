#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
from werkzeug.utils import secure_filename
from os import path, chmod, makedirs
from const import VARIABLE_STORE_DIR

class ImageRepository(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_INSTANCE"):
            cls._INSTANCE = super(ImageRepository, cls).__new__(cls)
        return cls._INSTANCE


    def __init__(self):
        self._PROJECT_IMAGE_BASE_PATH = path.join(VARIABLE_STORE_DIR, 'project')
        self._SKILL_IMAGE_BASE_PATH = path.join(VARIABLE_STORE_DIR,'skill')
        self._project_images = []
        self._skill_images = []
        self._rehash()


    def _rehash(self):
        self._project_images = glob.glob(path.join(self._PROJECT_IMAGE_BASE_PATH, '*'))
        self._skill_images = glob.glob(path.join(self._SKILL_IMAGE_BASE_PATH, '*'))

    
    def save_project_img(self, img_stream, filename):
        return self._save_img(img_stream, self._PROJECT_IMAGE_BASE_PATH, filename)


    def save_skill_img(self, img_stream, filename):
        return self._save_img(img_stream, self._SKILL_IMAGE_BASE_PATH, filename)


    def _save_img(self, img_stream, dst_dir, filename):
        if not path.exists(dst_dir):
            makedirs(dst_dir)
            # httpサーバとapiサーバの実行ユーザが異なるのでパーミッションを与える
            chmod(dst_dir, 0o777)

        file_path = path.join(dst_dir, secure_filename(filename))
        with open(file_path, 'wb') as f:
            f.write(img_stream.read())
            # httpサーバとapiサーバの実行ユーザが異なるのでパーミッションを与える
            chmod(file_path, 0o666)

        self._rehash()

        return file_path


    def get_project_images_name(self):
        names = []

        for img_path in self._project_images:
            names.append(path.basename(img_path))

        return names


    def get_project_image(self, img_name):
        with open(path.join(self._PROJECT_IMAGE_BASE_PATH, img_name), 'rb') as f:
            return f.read()

    
    def get_skill_images_name(self):
        names = []

        for img_path in self._skill_images:
            names.append(path.basename(img_path))
            
        return names


    def get_skill_image(self, img_name):
        with open(path.join(self._SKILL_IMAGE_BASE_PATH, img_name), 'rb') as f:
            return f.read()
