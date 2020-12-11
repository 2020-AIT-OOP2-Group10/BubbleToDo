from flask import Flask, request, render_template, jsonify
import json  # Python標準のJSONライブラリを読み込んで、データの保存等に使用する
import datetime # 日付でソートする際に使用

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # 日本語などのASCII以外の文字列を返したい場合は、こちらを設定しておく


# http://127.0.0.1:5000/get
@app.route('/get')
def get():

    # jsonデータを返す
    with open('todo-list.json') as f:
        json_data = json.load(f)

    return jsonify(json_data)


# http://127.0.0.1:5000/add
@app.route('/add', methods=["POST"])
def add():
    # jsonファイルに新規データを登録する

    # 1.jsonファイルを開く(add(get関数内を参考に))
    # 2.追加するデータを取得
    # 3.データをappendする
    # 4.jsonファイルに書き込む

    # todoリストのデータ自体は返さない
    pass


# http://127.0.0.1:5000/remove
@app.route('/remove')
def remove():
    # jsonファイルから選択されたデータを削除する

    # 1.jsonファイルを開く
    # 2.削除するデータのid配列を取得
    # 3.jsonデータの"id"項目が一致するものを削除
    # 4.jsonファイルに書き込む

    # todoリストのデータ自体は返さない
    pass


# http://127.0.0.1:5000/sort
@app.route('/sort')
def sort():
    with open('todo-list.json') as f:
        json_data = json.load(f)

    # 期限の近い順にソート
    sort_data = sorted(
        json_data,
        key=lambda x:
            datetime.date(
                datetime.datetime.strptime(x["timelimit"], "%Y/%m/%d").year,
                datetime.datetime.strptime(x["timelimit"], "%Y/%m/%d").month,
                datetime.datetime.strptime(x["timelimit"], "%Y/%m/%d").day
            )
    )

    # jsonファイルの内容は変更せずに、htmlの表示上で変える
    return jsonify(sort_data)


# http://127.0.0.1:5000/
@app.route('/')
def index():
    return(render_template("index.html"))


if __name__ == "__main__":
    # debugモードが不要の場合は、debug=Trueを消してください
    app.run(debug=True)
