import os
import uuid
import boto3
from flask import Flask, request, render_template_string

app = Flask(__name__)

s3_client = boto3.client('s3', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

UPLOAD_BUCKET = os.environ.get('UPLOAD_BUCKET')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>AI 影像辨識上傳系統</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; width: 100%; max-width: 400px; }
        input[type="file"] { margin: 20px 0; border: 1px solid #ccc; padding: 10px; width: 90%; border-radius: 5px;}
        button { background-color: #ff9900; color: white; border: none; padding: 12px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; margin-top: 10px; font-weight: bold;}
        button:hover { background-color: #e68a00; }
        .msg { margin-top: 15px; font-weight: bold; color: #28a745; background: #e8f5e9; padding: 10px; border-radius: 5px;}
        .err { margin-top: 15px; font-weight: bold; color: #dc3545; background: #fde8e8; padding: 10px; border-radius: 5px;}
    </style>
</head>
<body>
    <div class="card">
        <h2>📷 AI 影像分析流水線</h2>
        <p style="color: #666; font-size: 14px; margin-bottom: 20px;">上傳圖片後將自動觸發後端 AI 進行標籤辨識</p>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/jpeg, image/png" required>
            <button type="submit">上傳至 S3</button>
        </form>
        {% if msg %} <div class="msg">{{ msg }}</div> {% endif %}
        {% if err %} <div class="err">{{ err }}</div> {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if not UPLOAD_BUCKET:
            return render_template_string(HTML_TEMPLATE, err="系統錯誤：尚未設定 UPLOAD_BUCKET 環境變數！")
        
        file = request.files.get('file')
        if not file or file.filename == '':
            return render_template_string(HTML_TEMPLATE, err="請選擇檔案！")
            
        try:
            ext = file.filename.rsplit('.', 1)[-1].lower()
            unique_filename = f"upload_{uuid.uuid4().hex[:8]}.{ext}"
                 
            s3_client.upload_fileobj(file, UPLOAD_BUCKET, unique_filename)
            
            return render_template_string(HTML_TEMPLATE, msg=f"✅ 上傳成功！檔名：{unique_filename} (後端已觸發)")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, err=f"❌ S3 存取被拒或上傳失敗，請檢查 IAM 權限與環境變數：{str(e)}")

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)