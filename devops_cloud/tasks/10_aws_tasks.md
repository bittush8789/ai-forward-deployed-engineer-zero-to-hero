# Practice Tasks: Module 10 - AWS Infrastructure

This document outlines step-by-step tasks to practice AWS networking, identity control, and storage hardening using the AWS CLI.

---

## Task 1: Building a Custom VPC
*   **Goal**: Create a virtual network with a public subnet, internet gateway, and route table.
*   **Step-by-Step Instructions**:
    1. Create the VPC resource and save the output ID:
       ```bash
       VPC_ID=$(aws ec2 create-vpc --cidr-block 172.16.0.0/16 --query 'Vpc.VpcId' --output text)
       echo "VPC ID: $VPC_ID"
       ```
    2. Create a public subnet inside the VPC:
       ```bash
       SUBNET_ID=$(aws ec2 create-subnet --vpc-id "$VPC_ID" --cidr-block 172.16.1.0/24 --query 'Subnet.SubnetId' --output text)
       echo "Subnet ID: $SUBNET_ID"
       ```
    3. Create an Internet Gateway (IGW) and attach it to your VPC:
       ```bash
       IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
       aws ec2 attach-internet-gateway --vpc-id "$VPC_ID" --internet-gateway-id "$IGW_ID"
       ```
    4. Create a route table for the subnet:
       ```bash
       ROUTE_TABLE_ID=$(aws ec2 create-route-table --vpc-id "$VPC_ID" --query 'RouteTable.RouteTableId' --output text)
       ```
    5. Associate route path rules for outbound traffic:
       ```bash
       aws ec2 create-route --route-table-id "$ROUTE_TABLE_ID" --destination-cidr-block 0.0.0.0/0 --gateway-id "$IGW_ID"
       aws ec2 associate-route-table --subnet-id "$SUBNET_ID" --route-table-id "$ROUTE_TABLE_ID"
       ```
*   **Verification**:
    Verify the route table association and configuration:
    ```bash
    aws ec2 describe-route-tables --route-table-ids "$ROUTE_TABLE_ID"
    ```

---

## Task 2: Hardening S3 Buckets
*   **Goal**: Create an S3 storage bucket and restrict public access permissions.
*   **Step-by-Step Instructions**:
    1. Define a unique bucket name:
       ```bash
       BUCKET_NAME="my-enterprise-hardened-bucket-$(date +%s)"
       ```
    2. Create the bucket:
       ```bash
       aws s3api create-bucket --bucket "$BUCKET_NAME" --region us-east-1
       ```
    3. Block public access at the bucket level:
       ```bash
       aws s3api put-public-access-block \
         --bucket "$BUCKET_NAME" \
         --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
       ```
    4. Apply a bucket policy to enforce TLS connections:
       ```bash
       cat << EOF > /tmp/s3_policy.json
       {
         "Version": "2012-10-17",
         "Statement": [
           {
             "Sid": "EnforceSSLOnly",
             "Effect": "Deny",
             "Principal": "*",
             "Action": "s3:*",
             "Resource": [
               "arn:aws:s3:::$BUCKET_NAME",
               "arn:aws:s3:::$BUCKET_NAME/*"
             ],
             "Condition": {
               "Bool": {
                 "aws:SecureTransport": "false"
               }
             }
           }
         ]
       }
       EOF
       aws s3api put-bucket-policy --bucket "$BUCKET_NAME" --policy file:///tmp/s3_policy.json
       ```
*   **Verification**:
    Verify the bucket policy configurations:
    ```bash
    aws s3api get-bucket-policy --bucket "$BUCKET_NAME"
    ```
    Clean up the bucket:
    ```bash
    aws s3api delete-bucket-policy --bucket "$BUCKET_NAME"
    aws s3api delete-bucket --bucket "$BUCKET_NAME"
    ```
