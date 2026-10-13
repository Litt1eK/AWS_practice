# S3 → SQS → Lambda → S3

- main.py needs environment updates
- S3 Event Notifications need to be configured for S3 Bucket A
- SQS and Lambda IAM permissions required

1. Upload images to S3 Bucket A

2. S3 Bucket A triggers and sends event messages to SQS

3. SQS queues messages and triggers Lambda

4. Lambda processes the image messages from SQS

5. Lambda saves the processed image results to S3 Bucket B