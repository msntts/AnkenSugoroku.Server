#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import unittest
import json
import os

class PieceTest(unittest.TestCase):
    """
    API piecesに関するテスト
    """
    HOST = os.getenv('TEST_TARGET_HOST')

    _store = {}

    @classmethod
    def _util_store_piece(cls, piece):
        """
        前のテストで作った駒を参照するために保存
        """
        PieceTest._store = piece


    @classmethod
    def _util_get_piece(cls):
        return PieceTest._store


    @classmethod
    def _util_subset_in_dic(cls, dic, subset):
        for key in subset:
            if key not in dic:
                return False
            elif dic[key] != subset[key]:
                return False
            else:
                continue

        return True


    @classmethod
    def _util_subset_in_dict_array(cls, dic_arr, subset):
        for dic in dic_arr:
            if PieceTest._util_subset_in_dic(dic, subset):
                return True

        # ここまで来たら存在しなかった
        return False


    def test_001_post_pieces_with_invalid_parameter(self):
        """
        API
        - POST /pieces
        仕様
        1. 駒の作成
        2. パラメータ内の画像名は登録済みのものを指定すること
        期待値
        1. ステータスコード400が応答されること
        2. 駒が作成されないこと
        """
        # 存在しない画像を指定
        payload = {'name': 'test', 'url_img_project': 'not_exist.png', 'url_img_skill': 'not_exist.png'}
        response = requests.post(f'http://{PieceTest.HOST}/pieces/', data = json.dumps(payload))
        self.assertEqual(response.status_code, 400, response.json()) # 1

        # 駒リストにないことも確認
        response = requests.get(f'http://{PieceTest.HOST}/pieces/')
        self.assertFalse(PieceTest._util_subset_in_dict_array(response.json(), payload), response.json()) # 2


    def test_002_post_pieces_with_not_enough_parameter(self):
        """
        API
        - POST /pieces
        仕様
        1. 駒の作成
        2. すべてのパラメータが存在していること
        期待値
        1. ステータスコード400が応答されること
        2. 駒が作成されないこと
        """
        # nameがない
        payload = {'url_img_project': 'not_exist.png', 'url_img_skill': 'skill.jpg'}
        response = requests.post(f'http://{PieceTest.HOST}/pieces/', data = json.dumps(payload))
        self.assertEqual(response.status_code, 400, response.json()) # 1

        # 駒リストにないことも確認
        response = requests.get(f'http://{PieceTest.HOST}/pieces/')
        self.assertFalse(PieceTest._util_subset_in_dict_array(response.json(), payload), response.json()) # 2


    def test_003_post_pieces(self):
        """
        API
        - POST /pieces
        仕様
        1. 駒の作成
        期待値
        1. ステータスコード201が応答されること
        2. 指定した内容で駒が作成されること
        3. 駒の位置が初期位置になっていること
        4. 作成した駒が駒リストに表示されること
        """
        payload = {'name': 'test', 'url_img_project': 'project-images/anken.png', 'url_img_skill': 'skill-images/skill.jpg'}
        response = requests.post(f'http://{PieceTest.HOST}/pieces/', data = json.dumps(payload))
        self.assertEqual(response.status_code, 201, response.json()) # 1

        created = response.json()
        self.assertTrue(PieceTest._util_subset_in_dic(created, payload), response.json()) # 2
       
        self.assertEqual(created['position'], 1) # 3

        # 生成した時の表示内容が駒リストに表示されることを確認
        response = requests.get(f'http://{PieceTest.HOST}/pieces/')
        self.assertIn(created, response.json(), response.json())

        # ここまで来たら成功
        # テストで作った駒を記憶しておく
        PieceTest._util_store_piece(created)


    def test_010_get_pieces(self):
        """
        API
        - GET /pieces
        仕様
        1. 駒リストの表示
        期待値
        1. ステータスコードが200であること
        2. 作成した駒が駒リストに表示されていること
        """
        piece = PieceTest._util_get_piece()

        response = requests.get(f'http://{PieceTest.HOST}/pieces/')
        self.assertEqual(response.status_code, 200, response.json())
        
        self.assertIn(piece, response.json(), response.json()) # 2


    def test_020_put_piece(self):
        """
        API
        - PUT /pieces/<piece_id>
        仕様
        1. piece_idで指定した駒の更新
        期待値
        1. ステータスコードが200であること
        2. 指定したパラメータで駒が更新されること
        3. 更新した駒が駒リストに表示されること
        """
        piece = PieceTest._util_get_piece()
        piece['name'] = 'updated' # nameを更新

        response = requests.put(f'http://{PieceTest.HOST}/pieces/' + str(piece['id']), data = json.dumps(piece))

        self.assertEqual(response.status_code, 200, response.json()) # 1

        self.assertDictEqual(piece, response.json()) # 2

        # 生成した時の表示内容が駒リストに表示されることを確認
        response = requests.get(f'http://{PieceTest.HOST}/pieces/')
        for listed in response.json():
            if listed['id'] == piece['id']: # 3
                self.assertDictEqual(piece, listed)
                # テスト成功したので駒を更新
                PieceTest._util_store_piece(piece)
                return 

        # ここに来たときはリストになかった場合
        self.fail()


    def test_030_get_pieces_with_id(self):
        """
        API
        - GET /piece/<piece_id>
        仕様
        1. piece_idで指定した駒の取得
        期待値
        1. ステータスコードが200であること
        2. 登録している駒が表示されること
        """
        piece = PieceTest._util_get_piece()
        response = requests.get(f'http://{PieceTest.HOST}/pieces/' + str(piece['id']))

        self.assertEqual(response.status_code, 200, response.json()) # 1

        self.assertDictEqual(piece, response.json()) # 2


    def test_031_get_pieces_with_invalid_id(self):
        """
        API
        - GET /piece/<piece_id>
        仕様
        1. piece_idで指定した駒の取得
        2. piece_idは登録済みのものであること
        期待値
        1. ステータスコードが400であること
        """
        response = requests.get(f'http://{PieceTest.HOST}/pieces/100')

        self.assertEqual(response.status_code, 400, response.json()) # 1


    def test_040_put_pieces_position_with_id(self):
        """
        API
        - PUT /piece/<piece_id>/position
        仕様
        1. piece_idで指定した駒の位置情報更新
        期待値
        1. ステータスコードが200であること
        2. 指定したパラメータで駒が更新されること
        3. 更新した駒が駒リストに表示されること
        """
        payload = {
            'from_id': 1,
            'to_id': 2
        }
        piece = PieceTest._util_get_piece()
        piece['position'] = 2 # payloadに合わせて更新

        response = requests.put(f'http://{PieceTest.HOST}/pieces/' + str(piece['id']) + '/position', data = json.dumps(payload))

        self.assertEqual(response.status_code, 200, response.json()) # 1

        self.assertDictEqual(piece, response.json()) # 2

        response = requests.get(f'http://{PieceTest.HOST}/pieces/')
        for listed in response.json():
            if listed['id'] == piece['id']: # 3
                self.assertDictEqual(piece, listed)
                # テスト成功したので駒を更新
                PieceTest._util_store_piece(piece)
                return 

        # ここに来たときはリストになかった場合
        self.fail()


    def test_050_delete_pieces_with_invalid_id(self):
        """
        API
        - DELETE /piece/<piece_id>/
        仕様
        1. piece_idで指定した駒の削除
        2. 存在するpiece_idを指定すること
        期待値
        1. ステータスコードが400であること
        """
        response = requests.delete(f'http://{PieceTest.HOST}/pieces/100')

        self.assertEqual(response.status_code, 400, response.json()) # 1


    def test_051_delete_pieces_with_id(self):
        """
        API
        - DELETE /piece/<piece_id>/
        仕様
        1. piece_idで指定した駒の削除
        期待値
        1. ステータスコードが200であること
        2. 削除した駒が駒リストに表示されないこと
        """
        piece = PieceTest._util_get_piece()
        response = requests.delete(f'http://{PieceTest.HOST}/pieces/' + str(piece['id']))
        
        self.assertEqual(response.status_code, 200, response.json()) # 1

        response = requests.get(f'http://{PieceTest.HOST}/pieces/')

        for lisetd in response.json():
            if lisetd['id'] == piece['id']: # 2
                self.fail()

        # ここまで来たら削除成功
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
