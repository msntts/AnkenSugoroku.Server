#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .image_repository import ImageRepository
from os import path
import sys

# API用のファイルパス(RESTで指定されるpath)と実態のパスが異なるので本サービスで変換する
# API -> REPOSITORYでは、ファイル名のみを抽出しREPOSITORYへ渡す
# API <- REPOSITORYでは、ファイル名にAPI用のベースパスを付与しAPIへ返す
class ImageService():
    def __init__(self):
        self._image_rep = ImageRepository()
        self._PROJECT_IMG_API_BASE_PATH = 'project-images/'
        self._SKILL_IMG_API_BASE_PATH = 'skill-images/'

    
    def allowed_ext(self, filename):
        return path.splitext(filename)[1] in ['.jpg', '.jpeg', '.png']


    def save_project_img(self, img_stream, filename):
        return self._image_rep.save_project_img(img_stream, filename)


    def save_skill_img(self, img_stream, filename):
        return self._image_rep.save_skill_img(img_stream, filename)        


    def project_img_exist(self, api_filepath):
        if api_filepath.find(self._PROJECT_IMG_API_BASE_PATH) == 0:
            filename = path.basename(api_filepath)
            return filename in self._image_rep.get_project_images_name()
        else:
            return False


    def skill_img_exist(self, api_filepath):
        if api_filepath.find(self._SKILL_IMG_API_BASE_PATH) == 0:
            filename = path.basename(api_filepath)
            return filename in self._image_rep.get_skill_images_name()

    
    def get_project_images_name(self):
        images_name = []
        for img_name in self._image_rep.get_project_images_name():
            images_name.append(path.join(self._PROJECT_IMG_API_BASE_PATH, img_name))

        return images_name 


    def get_project_image(self, img_name):
        try:
            return self._image_rep.get_project_image(img_name)
        except:
            raise ValueError(f'{img_name}が見つかりませんでした。')


    def get_skill_images_name(self):
        images_name = []
        for img_name in self._image_rep.get_skill_images_name():
            images_name.append(path.join(self._SKILL_IMG_API_BASE_PATH, img_name))

        return images_name 


    def get_skill_image(self, img_name):
        try:
            return self._image_rep.get_skill_image(img_name)
        except:
            raise ValueError(f'{img_name}が見つかりませんでした。')     