#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from pytz import timezone
from .piece_repository import PieceRepository
from .piece_model import PieceModel
from .piece_history_repository import PieceHistoryRepository
from .piece_history_model import PieceHistoryModel
from .piece_command import PieceCommand
from .piece_position_command import PiecePositionCommand
from .piece_history_comment_command import PieceHistoryCommentCommand
from image.image_service import ImageService


class PieceService():
    def __init__(self):
        self._piece_rep = PieceRepository()
        self._piece_hist_rep = PieceHistoryRepository()
        self._image_serv = ImageService()


    def is_piece_exist(self, piece_id):
        return self._piece_rep.find_piece_by_id(piece_id) is not None


    def get_all_pieces(self):
        return self._piece_rep.get_all_pieces()


    def get_piece(self, piece_id):
        if self.is_piece_exist(piece_id):
            return self._piece_rep.find_piece_by_id(piece_id)
        else:
            self._raise_piece_id_not_found(piece_id)


    def create_piece(self, command):
        new_id =  self._number_new_piece_id()
        
        self._validatePieceCommand(new_id, command)

        self._piece_rep.set_piece(
            new_id,
            command.get_name(),
            command.get_url_img_project(),
            command.get_url_img_skill(),
            1) # 1=初期ポジション

        return self._piece_rep.find_piece_by_id(new_id)


    def update_piece(self, piece_id, command):
        self._validatePieceCommand(piece_id, command)

        piece = self._piece_rep.find_piece_by_id(piece_id)

        if piece is not None:
            self._piece_rep.set_piece(
                piece.get_id(),
                command.get_name(),
                command.get_url_img_project(),
                command.get_url_img_skill(),
                piece.get_position())

            return self._piece_rep.find_piece_by_id(piece_id)
        else:
            self._raise_piece_id_not_found(piece_id)


    def update_piece_position(self, piece_id, command):
        piece = self._piece_rep.find_piece_by_id(piece_id)

        if piece is not None:
            # pieceモデルの現在地を更新
            self._piece_rep.set_piece(
                piece.get_id(),
                piece.get_name(),
                piece.get_url_img_project(),
                piece.get_url_img_skill(),
                command.get_to_id())

            # 履歴を追加(タイムスタンプはサーバで押す)
            ja = timezone('Asia/Tokyo')
            self._piece_hist_rep.set_piece_history(
                piece.get_id(),
                self._number_new_piece_history_id(piece.get_id()),
                datetime.now(tz = ja).strftime('%Y-%m-%dT%H:%M'),
                command.get_from_id(),
                command.get_to_id(),
                '')

            return self.get_piece(piece.get_id())
        else:
            self._raise_piece_id_not_found(piece_id)


    def remove_piece(self, piece_id):
        if self.is_piece_exist(piece_id):
            # pieceを先に消すと、historyのpiece_idが引けなくなるので先にhistoryから消す
            if self.is_piece_histories_exist(piece_id):
                self._piece_hist_rep.remove_all_piece_histories(piece_id)

            self._piece_rep.remove_piece(piece_id)
        else:
            self._raise_piece_id_not_found(piece_id)


    def remove_piece_history(self, piece_id, history_id):
        # historyが存在するかの確認。なかったら例外が飛ぶので処理中断
        history = self._get_piece_history(piece_id, history_id)

        self._piece_hist_rep.remove_piece_history(piece_id, history_id)


    def set_piece_history_comment(self, piece_id, history_id, command):
        # historyが存在するかの確認。なかったら例外が飛ぶので処理中断
        history = self._get_piece_history(piece_id, history_id)

        self._piece_hist_rep.set_piece_history(
            piece_id,
            history.get_history_id(),
            history.get_date(),
            history.get_move_from(),
            history.get_move_to(),
            command.get_comment())

        return self._get_piece_history(piece_id, history_id)


    def remove_piece_history_comment(self, piece_id, history_id):
        return self.set_piece_history_comment(
            piece_id, 
            history_id, 
            PieceHistoryCommentCommand({'comment':''}))


    def _get_piece_history(self, piece_id, history_id):
        histories = self._piece_hist_rep.get_piece_histories(piece_id)

        if histories is None:
            self._raise_piece_id_not_found(piece_id)

        for history in histories:
            if history.get_history_id() == history_id:
                return history

        self._raise_history_id_not_found(piece_id, history_id)


    def is_piece_histories_exist(self, piece_id):
        histories = self.get_histories(piece_id)
        return histories is not None and len(histories) > 0


    def get_histories(self, piece_id):
        if self.is_piece_exist(piece_id):
            return self._piece_hist_rep.get_piece_histories(piece_id)
        else:
            self._raise_piece_id_not_found(piece_id)


    def _validatePieceCommand(self, piece_id, command):
        err_msgs = []
        if not self._image_serv.project_img_exist(command.get_url_img_project()):
            err_msgs.append(f'ファイルパス{command.get_url_img_project()}にデータが存在しません。')

        if not self._image_serv.skill_img_exist(command.get_url_img_skill()):
            err_msgs.append(f'ファイルパス{command.get_url_img_skill()}にデータが存在しません。')

        if len(err_msgs) > 0:
            raise ValueError(err_msgs)


    def _number_new_piece_id(self):
        new_id = 0
        for piece in self._piece_rep.get_all_pieces():
            new_id = max(new_id, piece.get_id())

        return new_id + 1


    def _number_new_piece_history_id(self, piece_id):
        new_id = 0

        for history in self._piece_hist_rep.get_piece_histories(piece_id):
            new_id = max(new_id, history.get_history_id())

        return new_id + 1


    def _raise_piece_id_not_found(self, piece_id):
        raise ValueError(f'piece_id={piece_id}は存在しません。')


    def _raise_history_id_not_found(self, piece_id, history_id):
        raise ValueError(f'piece_id={piece_id} history_id={history_id}は存在しません。')
