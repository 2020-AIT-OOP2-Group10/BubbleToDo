// データを初期表示する
// 第9回課題と違ってチェックボックスを追加するのを忘れずに
// 引数は"app.py - @app.route"の引数。初期値は"/get"。
function init(app_route="/get") {
    // データの初期表示
    fetch(app_route).then(response => {
        //console.log(response)
        response.json().then((data) => {
            //console.log(data) // 取得されたレスポンスデータをデバッグ表示
            // データを表示させる
            const tableBody = document.querySelector("#todo-list > tbody")
            tableBody.innerHTML = ""
            
            data.forEach(elm => {
                // 1行づつ処理を行う
                //console.log(elm)
                let tr = document.createElement('tr')
                // チェックボックス
                let td = document.createElement('td')
                let checkbox = document.createElement('input')
                checkbox.type = "checkbox"
                checkbox.id = elm.id
                td.append(checkbox)
                tr.appendChild(td)
                // 内容
                td = document.createElement('td')
                let p = document.createElement('p')
                p.style.color = elm.color
                p.innerText = elm.content
                td.appendChild(p)
                tr.appendChild(td)
                // 期限
                td = document.createElement('td')
                td.innerText = elm.timelimit
                tr.appendChild(td)

                // 1行分をtableタグ内のtbodyへ追加する
                tableBody.appendChild(tr)
            })
        })
    })
}

init()

// データを追加する(LongMine)
document.getElementById("add-submit").addEventListener("click", (e) => {
    // ボタンイベントのキャンセル
    e.preventDefault()

    let ct = document.getElementById("content").value
    let tl = document.getElementById("time-limit").value
    if(!ct || !tl){
        return
    }
    // データを追加する処理
    let data = new FormData()
    data.append("ct", ct)
    data.append("tl", tl)
    // データを表示
    fetch('/add', { method: 'POST', body: data }).then(response => {
        console.log(response)
        init()
    })
        
})

// データを削除する(K19051)
document.getElementById("remove-submit").addEventListener("click", (e) => {
    // ボタンイベントのキャンセル
    e.preventDefault()

    // データを削除する処理
    // チェックボックスの入った要素のidを取得
    var n = document.getElementById("tbody").childElementCount;
    let checkedIds = [];
    for (i=1;i<=n;i++){
        todo=document.getElementById(i);
        if(todo.checked){
            checkedIds.push(i);
        }
    }

    let array = new FormData();
    array.append("checkedIds",checkedIds);

    // 取得したidを渡してpythonのjson削除関数を呼ぶ
    fetch('/remove', { method: 'POST', body: array, }).then(function (response) {
        // データを表示
        init()
    })
})

// データをソートする(KawaiKohsuke)
document.getElementById("sort-submit").addEventListener("click", (e) => {
    // ボタンイベントのキャンセル
    e.preventDefault()

    // データは既に"app.py"にてソートされている。表示する手順はinit()と同様である
    init(app_route="/sort")    
})
