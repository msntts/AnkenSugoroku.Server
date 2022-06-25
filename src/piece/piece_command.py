#!/usr/bin/env python
# -*- coding: utf-8 -*-
class PieceCommand:
    def __init__(self, json_payload):
        if json_payload is None:
            raise ValueError('Payloadが空です。')
        else:
            err_msgs = []
            if not 'name' in json_payload:
                err_msgs.append('nameキーは必須です。')
            if not 'url_img_skill' in json_payload:
                err_msgs.append('url_img_skillキーは必須です。')
            if not 'url_img_project' in json_payload:
                err_msgs.append('url_img_projectキーは必須です。')
            
            if len(err_msgs) > 0:
                raise ValueError(err_msgs)

        self._name = json_payload['name']
        self._url_img_project = json_payload['url_img_project']
        self._url_img_skill = json_payload['url_img_skill']


    def get_name(self):
        return self._name


    def get_url_img_project(self):
        return self._url_img_project


    def get_url_img_skill(self):
        return self._url_img_skill


