#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .piece_model import PieceModel
from .repository_util import load_json, save_json
import sys
class PieceRepository(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_INSTANCE"):
            cls._INSTANCE = super(PieceRepository, cls).__new__(cls)
        return cls._INSTANCE


    def __init__(self):
        self._PIECE_DATA_FILE = 'PieceData.json'
        self._pieces = load_json(self._PIECE_DATA_FILE)


    def get_all_pieces(self):
        pieces = []

        for id in self._pieces:
            pieces.append(self._to_piece_model(id))

        return pieces


    def find_piece_by_id(self, piece_id):
        key_id = str(piece_id)
        if key_id in self._pieces:
            return self._to_piece_model(key_id)
        else:
            return None


    def _to_piece_model(self, piece_id):
        return PieceModel(
                    int(piece_id),
                    self._pieces[piece_id]['name'],
                    self._pieces[piece_id]['url_img_project'],
                    self._pieces[piece_id]['url_img_skill'],
                    self._pieces[piece_id]['position']
                )


    def set_piece(self, piece_id, name, url_img_project, url_img_skill, position):
        piece_data = {
            'name': name,
            'url_img_project': url_img_project,
            'url_img_skill': url_img_skill,
            'position': position
        }
        key_id = str(piece_id)
        if key_id not in self._pieces:
            self._pieces[key_id] = {}

        self._pieces[key_id].update(piece_data)

        save_json(self._PIECE_DATA_FILE, self._pieces)


    def remove_piece(self, piece_id):
        del self._pieces[str(piece_id)]

        save_json(self._PIECE_DATA_FILE, self._pieces)
