# ankenserv.py rest api仕様
開発中にデータの準備でPOSTMANとかそういうので投げつけるときの参考に。
URLで終端に/が歩かないかで動かなかったりするので、この資料中のURLでダメだったときは/を付けたり消したりしてみてください。(not foundとか言われます)

## GET /pieces/
### リクエストパラメータ
なし

### レスポンス
PieceModelの配列
```json
[
  {
    "id": 1,
    "name": "first",
    "position": 4,
    "url_img_project": "project-images/yuusya_game.png",
    "url_img_skill": "skill-images/game_ken.png"
  },
  {
    "id": 2,
    "name": "second2",
    "position": 5,
    "url_img_project": "project-images/yuusya_game.png",
    "url_img_skill": "skill-images/game_ken.png"
  }
]
```

## POST /pieces/
### リクエストパラメータ
httpボディのJSONで生成する駒情報を与える。  
引数の```url～```は後述の画像リストからコピーしたものを使うこと。(存在しない画像を指定すると失敗する)  

```json
{
    "name": "first",
    "url_img_project": "project-images/yuusya_game.png",
    "url_img_skill": "skill-images/game_ken.png"   
}
```

### レスポンス
作成したPieceModel。piece_idはサーバサイドで採番される。  
positionは初期値の1(typescriptのコードに書いてあった)
```json
  {
    "id": 1,
    "name": "first",
    "position": 1,
    "url_img_project": "project-images/yuusya_game.png",
    "url_img_skill": "skill-images/game_ken.png"
  }
```

## PUT /pieces/\<int:piece_id\>
### リクエストパラメータ
urlパラメータに更新したい駒のpiece_idを入力。
更新可能なデータをhttpボディのJSONで与える。  
※手を抜いたので、更新しなくても以下のデータはすべて入力すること。
```json
{
    "name": "first", 
    "url_img_project": "project-images/yuusya_game.png",
    "url_img_skill": "skill-images/game_ken2.png" // \<- ここを変えたい  
}
```

### レスポンス
更新後のPieceModel。
```json
  {
    "id": 1,
    "name": "first",
    "position": 1,
    "url_img_project": "project-images/yuusya_game.png",
    "url_img_skill": "skill-images/game_ken2.png"
  }
```

## GET /pieces/\<int:piece_id\>
### リクエストパラメータ
urlパラメータにデータを取得したい駒のpiece_idを入力。

### レスポンス
該当するpiece_idのPieceModel
```json
  {
    "id": 1,
    "name": "first",
    "position": 1,
    "url_img_project": "project-images/yuusya_game.png",
    "url_img_skill": "skill-images/game_ken2.png"
  }
```

## DELETE /pieces/\<int:piece_id\>
### リクエストパラメータ
urlパラメータにデータを削除したい駒のpiece_idを入力。

### レスポンス
消しましたメッセージ
```json
{
    "message": "piece_id 2 is deleted."
}
```


## PUT /pieces/\<int:piece_id\>/position
### リクエストパラメータ
urlパラメータに移動させた駒のpiece_idを入力。
駒の移動情報をhttpボディのJSONで与える。
```json
{
    "from_id": 1,
    "to_id": 2
}
```

### レスポンス
移動後のPieceMode
```json
  {
    "id": 1,
    "name": "first",
    "position": 2,
    "url_img_project": "project-images/yuusya_game.png",
    "url_img_skill": "skill-images/game_ken2.png"
  }
```

## POST /project-images/
### リクエストパラメータ
案件画像データをPOSTする。詳細は、テストコード(docker/runtime_testあたり)参照。

### レスポンス
アップロードされましたメッセージ。この時出ているのはファイル名だけなので注意。
```json
{
    "messege": "game_ken2.png is uploaded."
}
```

## GET /project-images/
### リクエストパラメータ
なし

### レスポンス
案件画像名の配列。PieceModelのurl_img_projectにはこれで表示されている名前を使ってください。
```json
[
  "project-images/yuusya_game.png",
  "project-images/anken.png",
  "project-images/project-images_anken.png"
]
```

## GET /project-images/\<img_name\>
### リクエストパラメータ
(これは基本的にアプリだけが使う)  
urlパラメータに画像名(↑で取得したもの)を入力。

### レスポンス
画像のバイナリデータ。

## POST /skill-images/
### リクエストパラメータ
技術画像データをPOSTする。詳細は、テストコード(docker/runtime_testあたり)参照。

### レスポンス
アップロードされましたメッセージ。この時出ているのはファイル名だけなので注意。
```json
{
    "messege": "game_ken.png is uploaded."
}
```

## GET /skill-images/
### リクエストパラメータ
なし

### レスポンス
技術画像名の配列。PieceModelのurl_img_skillにはこれで表示されている名前を使ってください。
```json
[
  "skill-images/game_ken.png",
  "skill-images/skill-image.png"
]
```

## GET /skill-images/\<img_name\>
### リクエストパラメータ
(これは基本的にアプリだけが使う)  
urlパラメータに画像名(↑で取得したもの)を入力。

### レスポンス
画像のバイナリデータ。


## GET /histories/\<int:piece_id\>
### リクエストパラメータ
URLパラメータに履歴を取得したいpiece_idを入力。

### レスポンス
該当するpiece_idのHistoryModel配列。
```json
[
  {
    "comment": "",
    "date": "2021-05-05T06:31",
    "history_id": 1,
    "move_from": 3,
    "move_to": 4
  },
  {
    "comment": "",
    "date": "2021-05-05T06:54",
    "history_id": 2,
    "move_from": 2,
    "move_to": 3
  }
]
```

## POST /histories/\<int:piece_id\>/\<int:history_id\>
### リクエストパラメータ
URLパラメータに履歴を更新したいpiece_idと、更新対象のhistory_idを入力。
をhttpボディのJSONで与える。  
```json
{
    "comment": "移動しました"
}
```

### レスポンス
更新後のHistoryModel。
```json
  {
    "comment": "移動しました",
    "date": "2021-05-05T06:31",
    "history_id": 1,
    "move_from": 3,
    "move_to": 4
  }
```

## DELETE /histories/\<int:piece_id\>/\<int:history_id\>
### リクエストパラメータ
URLパラメータに履歴を削除したいpiece_idと、更新対象のhistory_idを入力。

### レスポンス
履歴を削除しましたメッセージ。
```json
{
    "message": "piece_id=1 history_id=1 is deleted."
}
```

## DELETE /histories/\<int:piece_id\>/\<int:history_id\>/comment
### リクエストパラメータ
URLパラメータに履歴中のコメントを削除したいpiece_idと、更新対象のhistory_idを入力。

### レスポンス
履歴を削除しましたメッセージ。
```json
{
    "message": "comment piece_id=1 history_id=1 is deleted."
}
```

~fin.~