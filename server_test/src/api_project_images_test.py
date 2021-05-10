#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import unittest
import json
import os

class ProjectImageTest(unittest.TestCase):
    """
    API project-imagesに関するテスト
    """
    HOST = os.getenv('TEST_TARGET_HOST')

    def test_001_post_project_image(self):
        """
        API
        - POST /project-images
        仕様
        1. 案件用画像の登録
        期待値
        1. ステータスコード200が応答されること
        2. 登録した画像(anken.png)が画面リストに出力されること
        """
        with open('resource/anken.png', 'rb') as f:
            file = {'project': f}
            response = requests.post(f'http://{ProjectImageTest.HOST}/project-images/', files = file)
        self.assertEqual(response.status_code, 200, response.json()) # 1

        response = requests.get(f'http://{ProjectImageTest.HOST}/project-images/')
        self.assertIn('project-images/anken.png', response.json()) # 2

    
    def test_002_post_invalid_prameter(self):
        """
        API
        - POST /project-images
        仕様
        1. 案件用画像の登録
        2. POSTパラメータがprojectであること
        期待値
        1. ステータスコード400が応答されること
        """
        with open('resource/anken.png', 'rb') as f:
            file = {'hoge': f}
            response = requests.post(f'http://{ProjectImageTest.HOST}/project-images/', files = file)
        self.assertEqual(response.status_code, 400, response.json()) # 1


    def test_003_post_denied_image(self):
        """
        API
        - POST /project-images
        仕様
        1. 案件用画像の登録
        2. 許容する拡張子はjpg、jpeg、png
        期待値
        1. ステータスコード415が応答されること
        """
        with open('resource/bad.txt', 'rb') as f:
            file = {'project': f}
            response = requests.post(f'http://{ProjectImageTest.HOST}/project-images/', files = file)
        self.assertEqual(response.status_code, 415, response.json()) # 1


    def test_010_get_project_images(self):
        """
        API
        - GET /project-images
        仕様
        1. 案件用画像一覧の取得
        期待値
        1. ステータスコードが200であること
        2. 登録した画像(anken.png)が画面リストに出力されること
        """
        response = requests.get(f'http://{ProjectImageTest.HOST}/project-images/')
        self.assertIn('project-images/anken.png', response.json())


if __name__ == '__main__':
    unittest.main()
