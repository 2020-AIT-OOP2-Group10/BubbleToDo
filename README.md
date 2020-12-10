# BubbleToDo
ToDoリスト

# 内部ディレクトリ構造
<pre>
Repository/
  ├ static/
  |   ├ bubbletodo.css
  |   └ main.js
  ├ templates/
  |   └ index.html
  ├ app.py
  └ todo-list.json
</pre>

|  ファイル  |  内容  |
| ---- | ---- |
|  bubbletodo.css  |  index.htmlに適用するCSS  |
|  main.js  |  index.html内のフォームの動作を定義するJavaScriptプログラム  |
|  index.html  |  ToDoリストおよびバブルUIを表示するHTML  |
|  app.py  |  Flaskルーティングとjsonファイルに対する操作を行うPythonプログラム  |
|  todo-list.json  |  ToDoリストのデータが保存されているJSONファイル  |

## todo-list.jsonの内容例

<pre>
[
    {
        "id": 1,
        "content": "内容",
        "timelimit": "2020/12/10",
        "color": "#ff0000"
    }
]
</pre>

|  キー  |  値  |
| ---- | ---- |
|  id  |  データ識別用ID。削除時に使用。整数型  |
|  content  |  ToDoリストの内容。文字列型。  |
|  timelimit  |  ToDoの期限。文字列型。  |
|  color  |  ToDoとバブルを対応づけるための色。文字列型でカラーコードが保存される。  |

# バージョン

- Python:3.5.8
- Flask:1.1.2
- Jinja2:2.11.2

# 実行方法

1. Repositoryのディレクトリに移動し、以下のコマンドを実行
<pre>$ python3 app.py</pre>

2. ブラウザにて、127.0.0.1:5000またはlocalhost:5000にアクセス
