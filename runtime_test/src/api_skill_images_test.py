#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import unittest
import json
import os

class SkillImageTest(unittest.TestCase):
    """
    API skill-imagesに関するテスト
    """
    HOST = os.getenv('TEST_TARGET_HOST')

    def test_001_post_skill_image(self):
        """
        API
        - POST /skill-images
        仕様
        1. 案件用画像の登録
        期待値
        1. ステータスコード200が応答されること
        2. 登録した画像(skill.jpg)が画面リストに出力されること
        """
        with open('resource/skill.jpg', 'rb') as f:
            file = {'skill': f}
            response = requests.post(f'http://{SkillImageTest.HOST}/skill-images/', files = file)
        self.assertEqual(response.status_code, 200) # 1

        response = requests.get(f'http://{SkillImageTest.HOST}/skill-images/')
        self.assertIn('skill-images/skill.jpg', response.json()) # 2


    def test_002_post_invalid_prameter(self):
        """
        API
        - POST /skill-images
        仕様
        1. 案件用画像の登録
        2. POSTパラメータがskillであること
        期待値
        1. ステータスコード400が応答されること
        """
        with open('resource/skill.jpg', 'rb') as f:
            file = {'hoge': f}
            response = requests.post(f'http://{SkillImageTest.HOST}/skill-images/', files = file)
        self.assertEqual(response.status_code, 400, response.json()) # 1


    def test_003_post_denied_image(self):
        """
        API
        - POST /skill-images
        仕様
        1. 案件用画像の登録
        2. 許容する拡張子はjpg、jpeg、png
        期待値
        1. ステータスコード415が応答されること
        """
        with open('resource/bad.txt', 'rb') as f:
            file = {'skill': f}
            response = requests.post(f'http://{SkillImageTest.HOST}/skill-images/', files = file)
        self.assertEqual(response.status_code, 415, response.json()) # 1


    def test_010_get_skill_images(self):
        """
        API
        - GET /skill-images
        仕様
        1. 案件用画像一覧の取得
        期待値
        1. ステータスコードが200であること
        2. 登録した画像(skill.jpg)が画面リストに出力されること
        """
        response = requests.get(f'http://{SkillImageTest.HOST}/skill-images/')
        self.assertEqual(response.status_code, 200) # 1

        self.assertIn('skill-images/skill.jpg', response.json()) # 2


if __name__ == '__main__':
    unittest.main()
