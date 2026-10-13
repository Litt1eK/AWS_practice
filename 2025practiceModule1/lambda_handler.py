import json
import boto3
import os
from datetime import datetime

rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = os.environ.get('TABLE_NAME')

def lambda_handler(event, context):
    print("收到觸發事件：", json.dumps(event))
    
  
    if not TABLE_NAME:
        print("錯誤：未設定 TABLE_NAME 環境變數")
        return {'statusCode': 500, 'body': 'Server Configuration Error: TABLE_NAME is missing'}
    table = dynamodb.Table(TABLE_NAME)

  
    for record in event.get('Records', []):
        s3_records = []
     
        if 'Sns' in record:
            try:
                sns_message = json.loads(record['Sns']['Message'])
            
                s3_records = sns_message.get('Records', [])
            except Exception as e:
                print(f"解析 SNS 訊息失敗: {e}")
                continue
        elif 's3' in record:
            s3_records = [record]
            
        for s3_record in s3_records:
            bucket = s3_record['s3']['bucket']['name']
            key = s3_record['s3']['object']['key']
            
            try:
                print(f"啟動 AI 辨識，目標圖片: {bucket}/{key}")
                response = rekognition.detect_labels(
                    Image={'S3Object': {'Bucket': bucket, 'Name': key}},
                    MaxLabels=5,  
                    MinConfidence=75
                )
                
                labels = [label['Name'] for label in response['Labels']]
                print(f"AI 辨識結果: {labels}")
                
                table.put_item(
                    Item={
                        'ImageID': key,
                        'UploadTime': datetime.now().isoformat(),
                        'Labels': labels,
                        'SourceBucket': bucket
                    }
                )
                print(f"✅ 成功將圖片 {key} 的標籤寫入 DynamoDB")
                
            except Exception as e:
                print(f"❌ 影像處理流水線失敗 ({key}): {str(e)}")

    return {'statusCode': 200, 'body': 'Pipeline Execution Completed'}