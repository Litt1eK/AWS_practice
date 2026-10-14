import boto3
import json
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'WorkDayMessages'

def lambda_handler(event, context):
    """
    WorkDay 留言板 API
    功能：接收前端傳來的 Email 與留言內容，並寫入 DynamoDB。
    """
    # 處理 CORS 預檢請求
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return build_response(200, "CORS OK")

    try:
        body_str = event.get('body', '{}')
        if not body_str:
            return build_response(400, "請求內容為空")
            
        body = json.loads(body_str)
        email = body.get('email')
        message = body.get('message')

        if not email or not message:
            return build_response(400, "缺少 email 或 message 參數")

        table = dynamodb.Table(TABLE_NAME)

        table.put_item(Item={
            'email': email,
            'message': message,
            'timestamp': str(datetime.now())
        })
        
        print(f"✅ 成功寫入留言 - 作者: {email}, 內容: {message}")
        return build_response(200, "留言成功送出至資料庫！")

    except Exception as e:
        print(f"❌ 系統錯誤: {str(e)}")
        return build_response(500, f"伺服器錯誤 (請檢查 IAM 權限): {str(e)}")


def build_response(status_code, message):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps({'message': message}, ensure_ascii=False)
    }