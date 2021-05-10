#!/usr/bin/env python
# -*- coding: utf-8 -*-
class PieceHistoryCommentCommand:
    def __init__(self, json_payload):
        if json_payload is None:
            raise ValueError('Payloadが空です。')
        else:
            if not 'comment' in json_payload:
                raise ValueError('commentキーは必須です。')

        self._comment = json_payload['comment']


    def get_comment(self):
        return self._comment
