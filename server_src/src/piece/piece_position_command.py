#!/usr/bin/env python
# -*- coding: utf-8 -*-
class PiecePositionCommand:
    def __init__(self, json_payload):
        if json_payload is None:
            raise ValueError('Payloadが空です。')
        else:
            err_msgs = []
            if not 'from_id' in json_payload:
                err_msgs.append('from_idキーは必須です。')
            if not 'to_id' in json_payload:
                err_msgs.append('to_idキーは必須です。')
            if len(err_msgs) > 0:
                raise ValueError(err_msgs)

        self._from_id = int(json_payload['from_id'])
        self._to_id = int(json_payload['to_id'])


    def get_from_id(self):
        return self._from_id


    def get_to_id(self):
        return self._to_id
