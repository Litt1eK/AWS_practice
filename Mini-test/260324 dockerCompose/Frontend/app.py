from flask import Flask, render_template_string
import requests
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    backend_url = os.environ.get('BACKEND_URL', 'http://localhost:8080')
    
    try:
        response = requests.get(f"{backend_url}/api/data")
        response.raise_for_status()
        data_dict = response.json() 
    
        display_text = json.dumps(data_dict, indent=4, ensure_ascii=False)
        
    except Exception as e:
        display_text = f"❌ 無法連線到 backend: {e}"

    html_template = """
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <title>ECS -> backend -> SQL 測試</title>
        <style>body { font-family: sans-serif; padding: 20px; }</style>
    </head>
    <body>
        <h1>🌐 前端容器</h1>
        <p>成功透過 backend 從 MySQL 撈出以下資料：</p>
        <pre style="background: #282c34; color: #61afef; padding: 15px; border-radius: 8px;">
{{ data }}
        </pre>
    </body>
    </html>
    """
    return render_template_string(html_template, data=display_text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)