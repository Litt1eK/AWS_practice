# ECS → Lambda → RDS

- frontend.py needs to update the API Gateway URL
- VPC and IAM configurations required

1. frontend runs on ECS

2. the ECS invokes Lambda

3. backend runs on lambda

4. create RDS using MySQL

5. backend connects to RDS

