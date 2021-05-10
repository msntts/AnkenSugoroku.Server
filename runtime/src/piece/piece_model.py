#!/usr/bin/env python
# -*- coding: utf-8 -*-
class PieceModel:
    def __init__(self, id, name, url_img_project, url_img_skill, position):
        self._id = id
        self._name = name
        self._url_img_project = url_img_project
        self._url_img_skill = url_img_skill
        self._position = position
    

    def get_id(self):
        return int(self._id)


    def get_name(self):
        return self._name


    def get_url_img_project(self):
        return self._url_img_project

    
    def get_url_img_skill(self):
        return self._url_img_skill


    def get_position(self):
        return self._position


    def to_dict(self):
        d = {}
        for attr in self.__dict__:
            # プライベートフィールドなので先頭に_がついているのを除去
            d[attr[1:]] = self.__dict__[attr]

        return d
