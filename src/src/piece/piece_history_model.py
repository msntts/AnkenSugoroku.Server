#!/usr/bin/env python
# -*- coding: utf-8 -*-

class PieceHistoryModel:
    def __init__(self, history_id, date, move_from, move_to, comment):
        self._history_id = history_id
        self._date = date
        self._move_from = move_from
        self._move_to = move_to
        self._comment = comment


    def get_history_id(self):
        return self._history_id


    def get_date(self):
        return self._date


    def get_move_from(self):
        return self._move_from


    def get_move_to(self):
        return self._move_to


    def get_comment(self):
        return self._comment


    def to_dict(self):
        d = {}
        for attr in self.__dict__:
            # プライベートフィールドなので先頭に_がついているのを除去
            d[attr[1:]] = self.__dict__[attr]

        return d
