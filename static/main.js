// データを初期表示する
// 第9回課題と違ってチェックボックスを追加するのを忘れずに
function init() {
    // データの初期表示
    fetch("/get").then(response => {
        console.log(response)
        response.json().then((data) => {
            console.log(data) // 取得されたレスポンスデータをデバッグ表示
            // データを表示させる
            const tableBody = document.querySelector("#todo-list > tbody")
            tableBody.innerHTML = ""
            
            data.forEach(elm => {
                // 1行づつ処理を行う
                console.log(elm)
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
                td.innerText = elm.content
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

    // データを追加する処理

    // データを表示
    init()
})

// データを削除する(K19051)
document.getElementById("remove-submit").addEventListener("click", (e) => {
    // ボタンイベントのキャンセル
    e.preventDefault()

    // データを削除する処理
    // チェックボックスの入った要素のidを取得
    // 取得したidを渡してpythonのjson削除関数を呼ぶ

    // データを表示
    init()
})

// データをソートする(KawaiKohsuke)
document.getElementById("sort-submit").addEventListener("click", (e) => {
    // ボタンイベントのキャンセル
    e.preventDefault()

    // データをソートする処理
    // jsonファイルの内容を変えずに表示上でソートする
})
