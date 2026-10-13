from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 指向 API Gateway 的 Invoke URL (不含結尾斜線)
BACKEND_URL = os.environ.get('BACKEND_URL', 'https://YOUR_URL.amazonaws.com')

@app.route('/')
def index():
    return '''
    <style>
        body { font-family: Arial; padding: 20px; }
        .box { border: 1px solid #ccc; padding: 15px; margin-bottom: 10px; border-radius: 5px; }
        button { cursor: pointer; margin-right: 5px; }
    </style>
    <h1>AWS 三層架構實作練習</h1>
    
    <div class="box">
        <h3>1. 測試 POST /api/user</h3>
        <input id="name" placeholder="輸入姓名">
        <button onclick="sendData()">送出資料</button>
    </div>

    <div class="box">
        <h3>2. 測試 GET /api/get</h3>
        <button onclick="getData()">抓取最新 5 筆資料</button>
        <ul id="user-list"></ul>
    </div>

    <p id="msg" style="color: blue;"></p>

    <script>
        async function sendData() {
            const name = document.getElementById('name').value;
            const res = await fetch('/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: name})
            });
            const data = await res.json();
            document.getElementById('msg').innerText = "POST 結果: " + data.message;
        }

        async function getData() {
            const res = await fetch('/list');
            const result = await res.json();
            const listEl = document.getElementById('user-list');
            listEl.innerHTML = ""; 
            
            if (result.data) {
                result.data.forEach(user => {
                    const li = document.createElement('li');
                    li.innerText = user.name;
                    listEl.appendChild(li);
                });
                document.getElementById('msg').innerText = "GET 成功！";
            } else {
                document.getElementById('msg').innerText = "GET 失敗: " + result.message;
            }
        }
    </script>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    user_data = request.json
    try:
        # 呼叫 API Gateway 的 POST 路由
        response = requests.post(f"{BACKEND_URL}/api/user", json=user_data, timeout=5)
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"message": f"連線失敗: {str(e)}"}), 500

@app.route('/list', methods=['GET'])
def list_users():
    try:
        # 呼叫 API Gateway 的 GET 路由
        response = requests.get(f"{BACKEND_URL}/api/get", timeout=5)
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"message": f"連線失敗: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)