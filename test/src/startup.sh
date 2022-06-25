#!/bin/bash

pip3 install -r requirements.txt

# wait for server initialization to complete
for c in 1 2 3 4 5; do
    code=$(curl -LI  http://anken_server_test_env:5000/pieces/ -o /dev/null -w "%{http_code}\n" -s)

    if [ $code == "200" ]; then
        break
    fi  

    echo retry $c times
    sleep 1
done

python3 api_project_images_test.py -v
python3 api_skill_images_test.py -v
python3 api_piece_test.py -v
python3 api_histories_test.py -v
