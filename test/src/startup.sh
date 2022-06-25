#!/bin/bash

pip3 install -r requirements.txt
python3 api_project_images_test.py -v
python3 api_skill_images_test.py -v
python3 api_piece_test.py -v
python3 api_histories_test.py -v
