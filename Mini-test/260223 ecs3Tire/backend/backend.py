import json
import pymysql 
import os

def lambda_handler(event, context):
    # 取得 HTTP 方法與路徑
    method = event.get('requestContext', {}).get('http', {}).get('method')
    path = event.get('rawPath') # HTTP API 專用路徑抓法
    
    print(f"DEBUG: 接收到請求 - 方法: {method}, 路徑: {path}")

    # 資料庫連線設定 (建議放在 Try 外面以便共用)
    try:
        conn = pymysql.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            database=os.environ.get('DB_NAME'),
            connect_timeout=5,
            cursorclass=pymysql.cursors.DictCursor # 讓結果以字典格式回傳
        )
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": f"資料庫連線失敗: {str(e)}"})}

    try:
        # --- 路由判斷 1: POST /api/user (存入資料) ---
        if method == 'POST' and '/api/user' in path:
            body = json.loads(event.get('body', '{}'))
            username = body.get('username')
            if not username:
                return {"statusCode": 400, "body": json.dumps({"message": "缺少 username"})}

            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (name) VALUES (%s)", (username,))
                conn.commit()
            return {"statusCode": 200, "body": json.dumps({"message": f"成功存入：{username}"})}

        # --- 路由判斷 2: GET /api/get (讀取最後 5 筆) ---
        elif method == 'GET' and '/api/get' in path:
            with conn.cursor() as cur:
                cur.execute("SELECT name FROM users ORDER BY id DESC LIMIT 5")
                result = cur.fetchall()
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "取得成功", "data": result}, ensure_ascii=False)
            }

        else:
            return {"statusCode": 404, "body": json.dumps({"message": f"找不到路由: {path}"})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": f"執行錯誤: {str(e)}"})}
    finally:
        conn.close()