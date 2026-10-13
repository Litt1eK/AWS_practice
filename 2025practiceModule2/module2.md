Module 2 - Serverless Membership Message Board System

Service： Amazon S3, Amazon CloudFront, Amazon Cognito, AWS Lambda, Amazon

DynamoDB, AWS IAM

## Objective

The goal of this challenge is to build an event-driven serverless membership message board system with global content acceleration. This system integrates Amazon CloudFront for content delivery, Amazon S3 for static website hosting, Amazon Cognito for identity management, AWS Lambda for backend logic, and Amazon DynamoDB for data storage.

The frontend source code (index.html, main.html) and the backend API logic (app.py) have been fully developed and provided to you. Only configuration values need to be updated. No modification to the core logic is required. Your objective is to build and configure the necessary AWS infrastructure, environment variables, and IAM permissions to ensure a secure and functional deployment.

In this architecture, the frontend is hosted on S3 and distributed via CloudFront. Users can register and log in through index.html, managed by Cognito. Upon successful authentication, users are redirected to main.html, where they can post messages that are processed by Lambda and stored in DynamoDB.

Note: Please refer to Table 1 for the required resource configuration.

Contestants must complete the following tasks:

## 1. Create DynamoDB Table

- Create an Amazon DynamoDB table to store user messages.

- Please follow the configuration in Table 1 for the table name and partition key.

## 2. Create Amazon S3 Bucket and Upload Assets

- Create an Amazon S3 bucket for static website hosting.

- Ensure that the bucket does not have public access enabled (Block all public access must be ON).

- Update the configuration settings (such as UserPoolId, ClientId, and API URL) in the provided index.html and main.html files, then upload them to the root of the bucket.

## 3. Configure Amazon Cognito Authentication

- Create a User Pool to manage member accounts. Sign-in Experience: Configure the user pool to allow users to sign in with their Email address.

- App Client Configuration (Critical):

- Create a Public Client suitable for Single Page Applications (SPA).

- Do NOT generate a client secret.


- In the Authentication Flows, ensure ALLOW_USER_SRP_AUTH is enabled.

- Configure Cognito to automatically send email verification codes to ensure users can confirm their accounts after registration.

## 4. Deploy Backend API (AWS Lambda)

- Create an AWS Lambda function using the provided app.py code and enable the Lambda Function URL feature.

## 5. Configure CloudFront Distribution with OAC

- Create an Amazon CloudFront Distribution and set the origin to your S3 bucket.

- Implement Origin Access Control (OAC) to protect the S3 bucket, ensuring that users can only access the website files through the CloudFront URL.

- Set the Default root object to index.html.

## 6. End-to-End Integration Test

- Access the frontend application via the CloudFront distribution URL.

- Verify the complete user journey: Registration Email Verification Login Redirect to main.html Submit Message.

- Confirm that submitted messages successfully appear as items in the DynamoDB table.

Contestants must complete all configurations as required and submit the final solution within the given timeframe.

*Table 1: Resource Configuration Parameters*

| Resource Category | Property | Value |
| --- | --- | --- |
| Amazon DynamoDB |   |   |
|   | Table Name | WorkDayMessages |
|   | Partition Key | email (String) |
|   | Capacity Mode | On-demand |
| Amazon S3 |   |   |
|   | Bucket Name | workday-web-[random-id] |
|   | Block Public Access | On (True) |


|   | Region | us-east-1 |
| --- | --- | --- |
| Amazon Cognito |   |   |
|   | User Pool Name | WorkDay-UserPool |
|   | App Client | Public Client (No Secret) |
|   | Auth Flows | ALLOW_USER_SRP_AUTH |
| AWS Lambda |   |   |
|   | Function Name | WorkDay-API |
|   | Runtime | Python 3.12 |
|   | Auth Type | Function URL (NONE) |
| Amazon CloudFront |   |   |
|   | Root Object | index.html |
|   | Origin Access | CloudFront OAC |
