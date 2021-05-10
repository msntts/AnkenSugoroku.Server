#!/usr/bin/env python
# -*- coding: utf-8 -*-
from const import VARIABLE_STORE_DIR
from os import path, remove, rename
import json 

_PIECE_BAK_DATA_EXT = '.bak'

def load_json(filename):
    load_path = path.join(VARIABLE_STORE_DIR, filename)
    backup_file = load_path + _PIECE_BAK_DATA_EXT

    try:
        # backupファイルがあったらそっちを正とする
        if path.exists(backup_file):
            # 今ある.jsonは信用ならないので削除
            if path.exists(load_path):
                remove(load_path)
            # backupファイルを本家とする
            rename(backup_file, load_path)

        with open(load_path, 'r') as f:
            return json.load(f)
    except:
        # もともとファイルがないときとか
        # backupが壊れてたらここに来る
        return {}


def save_json(filename, data):
    save_path = path.join(VARIABLE_STORE_DIR, filename)
    backup_file = save_path + _PIECE_BAK_DATA_EXT

    if path.exists(save_path):
        rename(save_path, backup_file)

    with open(save_path, 'w') as f:
        json.dump(data, f)

    # ここまで例外なしにきたら成功
    # backupファイルを消す
    if path.exists(backup_file):
        remove(backup_file)
