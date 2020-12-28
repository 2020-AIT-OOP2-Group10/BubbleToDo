from flask import Flask, request, render_template, jsonify, send_from_directory
import json  # Python標準のJSONライブラリを読み込んで、データの保存等に使用する
import datetime # 日付でソートする際に使用
import create_bubble_img
import random
import time
import os
import glob

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
    while True:
        # ランダムな色を生成
        color_str = "#"
        for i in range(6):
            color_str = color_str + random.choice('0123456789ABCDEF')

        # 白に近すぎる色は例外処理    
        color_r = int(color_str[1:3], 16)
        color_g = int(color_str[3:5], 16)
        color_b = int(color_str[5:7], 16)
        if color_r < 200 or color_g < 200 or color_b < 200:
            break

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
    with open('todo-list.json', 'w') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    #　json読み込み
    with open('todo-list.json','r',encoding="utf-8") as f:
        jsn = json.load(f)

    # バブル画像を作成
    for i in range(0,len(jsn)):
        jsn[i]["size"] = create_bubble_img.create_bubble_img(jsn[i]["content"], jsn[i]["timelimit"], jsn[i]["color"])

    # jsonファイルにsizeを付加してまた書き込む
    with open('todo-list.json', 'w') as f:
        json.dump(jsn, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


    return jsonify({
        "status": "append completed"
    })
    # todoリストのデータ自体は返さない
    pass


# http://127.0.0.1:5000/remove
@app.route('/remove', methods=["POST"])
def remove():
    # jsonファイルから選択されたデータを削除する
    
    content_text_list = []
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
    

    # 削除時はファイルの更新はいらなかった。
    # 代わりに作成された画像ファイルの不要なものを削除する
    #['./img/1234552wfag.png', './img/こんにいは.png', './img/はじめのいいいｓｄｈふぃｓふぇｓｆせｇ.png', './img/コンピュータ.png', './img/123452.png', './img/あいうれお.png', './img/一年後.png', './img/ランチ.png', './img/講義.png', './img/いあじｗｊだだ.png']
    # ./img/内の画像ファイルをすべて読み込みリスト化する。
    for i in range(len(json_data)):
        content_text_list.append(json_data[i]["content"])

    for row in glob.glob("./img/*"):
        #JSONに同じ文字列があるか判定 
        if row[6:-4] in content_text_list:
            pass
            # print(f"含まれる:{row[6:-4]}")
        else:
            # JSONファイル内に含まれていないものは削除する
            os.remove(f"{row}")




    # #　json読み込み
    # with open('todo-list.json','r',encoding="utf-8") as f:
    #     jsn = json.load(f)

    # # バブル画像を作成
    # for i in range(0,len(jsn)):
    #     jsn[i]["size"] = create_bubble_img.create_bubble_img(jsn[i]["content"], jsn[i]["timelimit"], jsn[i]["color"])

    return jsonify({
        "status": "append completed"
    })


# http://127.0.0.1:5000/sort/time-limit
@app.route('/sort/time-limit')
def sort_time_limit():
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


# http://127.0.0.1:5000/sort/content
@app.route('/sort/content')
def sort_content():
    with open('todo-list.json') as f:
        json_data = json.load(f)

    # 内容を昇順にソート
    sort_data = sorted(
        json_data,
        key=lambda x: x["content"]
    )

    return jsonify(sort_data)


# http://127.0.0.1:5000/sort/color
@app.route('/sort/color')
def sort_color():
    with open('todo-list.json') as f:
        json_data = json.load(f)

    # 色が濃い順(#FFFFFF -> #000000)にソート
    sort_data = sorted(
        json_data,
        key=lambda x: x["color"]
    )

    return jsonify(sort_data)




# http://127.0.0.1:5000/
@app.route('/')
def index():

    time.sleep(0.5)

    #　json読み込み
    with open('todo-list.json','r',encoding="utf-8") as f:
        jsn = json.load(f)

    # バブル画像を作成
    for i in range(0,len(jsn)):
        jsn[i]["size"] = create_bubble_img.create_bubble_img(jsn[i]["content"], jsn[i]["timelimit"], jsn[i]["color"])

    # jsonファイルにsizeを付加してまた書き込む
    with open('todo-list.json', 'w') as f:
        json.dump(jsn, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    return(render_template("index.html"))


@app.route('/upload_img/<filename>') 
def send_img(filename):
    return send_from_directory("./img", filename) 


# JSONファイルを外部(URL)から読み込めるように
"""
@app.route('/upload_json/<filename>') 
def send_json(filename):
    return send_from_directory("./", filename) 
"""

if __name__ == "__main__":
    # debugモードが不要の場合は、debug=Trueを消してください
    app.run(debug=True)
