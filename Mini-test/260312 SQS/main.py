import boto3
import os
import json
import uuid
from PIL import Image # 注意：在 AWS Lambda 中使用 Pillow 需要添加 Lambda Layer

# 初始化 AWS 客戶端
s3_client = boto3.client('s3')

# 【重要】這裡設定你的目標 S3 桶子名稱
# 你可以在 Lambda 控制台的 Configuration -> Environment variables 設定 DEST_BUCKET
# 或者直接把下面的字串改成你的桶子名稱，例如：DEST_BUCKET = "my-processed-photos-bucket"
DEST_BUCKET = os.environ.get('DEST_BUCKET', 'your-target-bucket-name')

def lambda_handler(event, context):
    """
    Lambda 進入點，處理來自 SQS 的訊息
    """
    for record in event['Records']:
        # 1. 解析 SQS 訊息內容
        # SQS 的 body 包含了 S3 原始事件的完整 JSON 資訊
        s3_event = json.loads(record['body'])
        
        if 'Records' not in s3_event:
            continue
            
        for s3_record in s3_event['Records']:
            # 來源資訊：自動從 S3 傳過來的資料中取得，不需要手動輸入
            source_bucket = s3_record['s3']['bucket']['name']
            source_key = s3_record['s3']['object']['key']
            
            # 只處理 jpg 檔案
            if not source_key.lower().endswith(('.jpg', '.jpeg')):
                print(f"跳過非 JPG 檔案: {source_key}")
                continue
            
            # 定義 Lambda 內部的暫存路徑 (/tmp 是 Lambda 唯一可寫入的暫存空間)
            download_path = f"/tmp/{uuid.uuid4()}{os.path.basename(source_key)}"
            upload_path = f"/tmp/processed-{os.path.basename(source_key)}"
            
            try:
                # 2. 從來源 S3 下載照片 (使用自動取得的 source_bucket)
                print(f"正在從來源桶子 {source_bucket} 下載檔案 {source_key}...")
                s3_client.download_file(source_bucket, source_key, download_path)
                
                # 3. 處理照片 (範例：轉為灰階並縮放)
                print(f"正在進行影像處理 (灰階 + 縮放)...")
                with Image.open(download_path) as img:
                    # 轉灰階
                    gray_img = img.convert('L')
                    # 縮放至 50%
                    width, height = gray_img.size
                    gray_img = gray_img.resize((width // 2, height // 2))
                    # 儲存到 Lambda 暫存區
                    gray_img.save(upload_path)
                
                # 4. 上傳到目標 S3 (使用我們設定的 DEST_BUCKET)
                # 我們可以指定存放在目標桶子的哪個資料夾下
                dest_key = f"processed_results/{os.path.basename(source_key)}"
                
                print(f"正在上傳處理後的檔案至目標桶子: {DEST_BUCKET}/{dest_key}")
                s3_client.upload_file(upload_path, DEST_BUCKET, dest_key)
                
                print(f"成功完成處理並儲存至目標 S3！")
                
            except Exception as e:
                print(f"處理過程發生錯誤: {str(e)}")
                # 拋出異常讓 SQS 知道處理失敗，訊息會回到隊列重試
                raise e
            finally:
                # 清理暫存檔，避免多次執行後佔用空間
                if os.path.exists(download_path):
                    os.remove(download_path)
                if os.path.exists(upload_path):
                    os.remove(upload_path)

    return {
        'statusCode': 200,
        'body': json.dumps('影像流水線處理成功')
    }