import pymysql

# VPC2 RDS Endpoint
DB_HOST = "your-rds-endpoint.aws.com" 

try:
    conn = pymysql.connect(host=DB_HOST, user="admin", password="password", connect_timeout=5)
    print("success")
    conn.close()
except Exception as e:
    print(f"failure: {e}")
