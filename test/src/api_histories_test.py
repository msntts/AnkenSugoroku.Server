#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import unittest
import json
import os

class HistoriesTest(unittest.TestCase):
    """
    API historiesに関するテスト
    """
    HOST = os.getenv('TEST_TARGET_HOST')

    _store = {}
    _histories = []

    @classmethod
    def _util_store_piece(cls, piece):
        """
        前のテストで作った駒を参照するために保存
        """
        HistoriesTest._store = piece


    @classmethod
    def _util_get_piece(cls):
        return HistoriesTest._store


    @classmethod
    def _util_store_histories(cls, histories):
        """
        前のテストで作った履歴を参照するために保存
        """
        HistoriesTest._histories = histories

    @classmethod
    def _util_get_histories(cls):
        return HistoriesTest._histories

    def test_001_get_histories_with_id(self):
        """
        API
        - GET /histories/<piece_id>
        仕様
        1. 駒の移動履歴の取得
        期待値
        1. ステータスコード200が応答されること
        2. 駒の履歴が表示されること
        """
        # 駒の作成
        payload = {'name': 'history', 'url_img_project': 'project-images/anken.png', 'url_img_skill': 'skill-images/skill.jpg'}
        response = requests.post(f'http://{HistoriesTest.HOST}/pieces/', data = json.dumps(payload))

        if response.status_code == 201:
            HistoriesTest._util_store_piece(response.json())
        else:
            self.fail()

        # 履歴の作成
        payload = {
            'from_id': 1,
            'to_id': 2
        }
        piece = HistoriesTest._util_get_piece()
        piece['position'] = 2 # payloadに合わせて更新

        response = requests.put(f'http://{HistoriesTest.HOST}/pieces/' + str(piece['id']) + '/position', data = json.dumps(payload))

        if piece != response.json():
            self.fail()

        # ここからテスト
        response = requests.get(f'http://{HistoriesTest.HOST}/histories/' + str(piece['id']))

        self.assertEqual(response.status_code, 200, response.json()) # 1

        histories = response.json()
        # 今履歴は1個だけのはずなので、[0]を検査
        self.assertEqual(histories[0]['comment'], "") # 2
        self.assertRegex(histories[0]['date'], "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}")
        self.assertEqual(histories[0]['history_id'], 1)
        self.assertEqual(histories[0]['move_from'], 1)
        self.assertEqual(histories[0]['move_to'], 2)

        # ここまで来たらOK。履歴を更新する
        HistoriesTest._util_store_histories(histories)


    def test_002_get_histories_with_invalid_id(self):
        """
        API
        - GET /histories/<piece_id>
        仕様
        1. 駒の移動履歴の取得
        2. piece_idは登録済みのものであること
        期待値
        1. ステータスコード400が応答されること
        """
        response = requests.get(f'http://{HistoriesTest.HOST}/histories/100')

        self.assertEqual(response.status_code, 400, response.json()) # 1


    def test_010_put_histories_with_ids(self):
        """
        API
        - PUT /histories/<piece_id>/<history_id>
        仕様
        1. 駒 移動履歴のコメントを更新
        期待値
        1. ステータスコード200が応答されること
        2. コメントが更新されること
        3. 更新した移動履歴が表示されること
        """
        payload = {'comment': '移動しました'}
        piece = HistoriesTest._util_get_piece()
        histories = HistoriesTest._util_get_histories()
        # 更新後のあるべき履歴
        history = histories[0]
        history['comment'] = '移動しました' 
        response = requests.put(f'http://{HistoriesTest.HOST}/histories/' 
        + str(piece['id']) + '/' + str(histories[0]['history_id']), json.dumps(payload))

        self.assertEqual(response.status_code, 200, response.json()) # 1

        self.assertEqual(history, response.json()) # 2

        response = requests.get(f'http://{HistoriesTest.HOST}/histories/' + str(piece['id']))

        self.assertIn(history, response.json()) # 3

        # ここまで来たら更新成功。履歴を更新
        HistoriesTest._util_store_histories(response.json())


    def test_011_put_histories_with_invalid_piece_id(self):
        """
        API
        - PUT /histories/<piece_id>/<history_id>
        仕様
        1. 駒 移動履歴のコメントを更新
        2. piece_idは登録済みのものであること
        期待値
        1. ステータスコード400が応答されること
        """

        payload = {'comment': '不正なpiece_idです'}
        histories = HistoriesTest._util_get_histories()
        # 更新後のあるべき履歴
        history = histories[0]
        response = requests.put(f'http://{HistoriesTest.HOST}/histories/100/1/' 
        + '/' + str(histories[0]['history_id']), json.dumps(payload))


    def test_012_put_histories_with_invalid_history_id(self):
        """
        API
        - PUT /histories/<piece_id>/<history_id>
        仕様
        1. 駒 移動履歴のコメントを更新
        2. history_idは登録済みのものであること
        期待値
        1. ステータスコード400が応答されること
        2. 駒 移動履歴のコメントが更新されないこと
        """
        payload = {'comment': '不正なhistory_idです'}
        piece = HistoriesTest._util_get_piece()
        histories = HistoriesTest._util_get_histories()
        # 更新後のあるべき履歴
        history = histories[0]
        response = requests.put(f'http://{HistoriesTest.HOST}/histories/' 
        + str(piece['id']) + '/100', json.dumps(payload))

        self.assertEqual(response.status_code, 400, response.json()) # 1

        response = requests.get(f'http://{HistoriesTest.HOST}/histories/' + str(piece['id']))

        # historyは更新前のもの
        self.assertIn(history, response.json()) # 2

        # ここまで来たら更新成功。履歴を更新
        HistoriesTest._util_store_histories(response.json())        


    def test_020_delete_histories_comment_with_ids(self):
        """
        API
        - DELETE /histories/<piece_id>/<history_id>/comment
        仕様
        1. 駒 移動履歴のコメントを削除
        期待値
        1. ステータスコード200が応答されること
        2. history_idで指定した駒 移動履歴のコメントが削除されること
        """
        piece = HistoriesTest._util_get_piece()
        histories = HistoriesTest._util_get_histories()
        history = histories[0]
        # 削除後のあるべきコメントに更新
        history['comment'] = ''
        response = requests.delete(f'http://{HistoriesTest.HOST}/histories/' 
        + str(piece['id']) + '/' + str(histories[0]['history_id']) + '/comment')

        self.assertEqual(response.status_code, 200) # 1

        response = requests.get(f'http://{HistoriesTest.HOST}/histories/' 
        + str(piece['id']))

        self.assertIn(history, response.json(), response.json())

        # ここまで来たらコメント削除成功。履歴を更新
        HistoriesTest._util_store_histories(response.json())


    def test_030_delete_histories_with_ids(self):
        """
        API
        - DELETE /histories/<piece_id>/<history_id>
        仕様
        1. 駒 移動履歴を削除
        期待値
        1. ステータスコード200が応答されること
        2. history_idで指定した駒の移動履歴が削除されること
        """
        piece = HistoriesTest._util_get_piece()
        histories = HistoriesTest._util_get_histories()
        history = histories[0]
        response = requests.delete(f'http://{HistoriesTest.HOST}/histories/' 
        + str(piece['id']) + '/' + str(histories[0]['history_id']))

        self.assertEqual(response.status_code, 200) # 1

        response = requests.get(f'http://{HistoriesTest.HOST}/histories/' 
        + str(piece['id']))

        self.assertNotIn(history, response.json(), response.json())


if __name__ == '__main__':
    unittest.main()
