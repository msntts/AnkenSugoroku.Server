#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .piece_history_model import PieceHistoryModel
from .repository_util import load_json, save_json

class PieceHistoryRepository:
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_INSTANCE"):
            cls._INSTANCE = super(PieceHistoryRepository, cls).__new__(cls)
        return cls._INSTANCE


    def __init__(self):
        self._HISTORIES_DATA_FILE = 'histories.json'
        self._histories = load_json(self._HISTORIES_DATA_FILE)


    def get_piece_histories(self, piece_id):
        histories = []
        key_piece_id = str(piece_id)

        if key_piece_id in self._histories:
            for key_history_id in self._histories[key_piece_id]:
                histories.append(PieceHistoryModel(
                    int(key_history_id),
                    self._histories[key_piece_id][key_history_id]['date'],
                    int(self._histories[key_piece_id][key_history_id]['move_from']),
                    int(self._histories[key_piece_id][key_history_id]['move_to']),
                    self._histories[key_piece_id][key_history_id]['comment']))

        return histories
        

    def set_piece_history(self, piece_id, history_id, date, move_from, move_to, comment):
        key_piece_id = str(piece_id)
        key_hst_id = str(history_id)
        if not key_piece_id in self._histories:
            self._histories[key_piece_id] = {}

        if not key_hst_id in self._histories[key_piece_id]:
            self._histories[key_piece_id][key_hst_id] = {}

        self._histories[key_piece_id][key_hst_id] = {
            'date': date, 
            'move_from': move_from, 
            'move_to': move_to,
            'comment': comment
        }

        save_json(self._HISTORIES_DATA_FILE, self._histories)


    def remove_all_piece_histories(self, piece_id):
        del self._histories[str(piece_id)]

        save_json(self._HISTORIES_DATA_FILE, self._histories)


    def remove_piece_history(self, piece_id, history_id):
        del self._histories[str(piece_id)][str(history_id)]

        save_json(self._HISTORIES_DATA_FILE, self._histories)

