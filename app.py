from flask import Flask, request, render_template, jsonify
import json  # Python標準のJSONライブラリを読み込んで、データの保存等に使用する
import datetime # 日付でソートする際に使用
import random

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
    with open('todo-list.json') as f:
        json_data = json.load(f)

    # 2.追加するデータを取得
    content_name = request.form.get('ct')
    timelimit = request.form.get('tl')
    # 3.データをappendする
    color_str = "#"
    for i in range(6):
        color_str = color_str + random.choice('0123456789ABCDEF')

    item = {}
    item["id"] = len(json_data) + 1
    item["content"] = content_name
    item["timelimit"] = timelimit.replace('-','/')
    item["color"] = color_str
    json_data.append(item)
    # 4.jsonファイルに書き込む
    print(json_data)
    with open('todo-list.json', 'w') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    return jsonify({
        "status": "append completed"
    })
    # todoリストのデータ自体は返さない

# http://127.0.0.1:5000/remove
@app.route('/remove', methods=["POST"])
def remove():
    # jsonファイルから選択されたデータを削除する
    
    # 1.jsonファイルを開く
    with open('todo-list.json') as f:
        json_data = json.load(f)

    # 2.削除するデータのid配列を取得(str型→list型)
    removeIds_unique = request.form.get('checkedIds')
    removeIds = removeIds_unique.split(',')

    # 3.jsonデータの"id"項目が一致するものを削除
    for e in removeIds:
        for i in range(len(json_data)):
            if json_data[i]['id'] == int(e):
                del json_data[i]
                break

    # 4.jsonファイルのidを整列
    count = 1
    for e in range(len(json_data)):
        json_data[e]['id'] = count
        count = count + 1
        
    # 5.jsonファイルに書き込む
    with open('todo-list.json', 'w') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    return jsonify({
        "status": "append completed"
    })


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
