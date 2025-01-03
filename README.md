# DevOps course final project
## Includes
- Python code application
- Docker as the python container
- github actions for CI/CD
- IaC implmented by Terraform over AWS
- Kubernetes
- Helm

## Step by step to construct the project
1. vim ~/.aws/credentials (from AWS CLI)
2. Update next github secrets:
    1. Copy the SSH key of the cloud access to  "SSH_KEY"
    2. Copy the aws_access_key_id to "AWS_ID" (use echo -n '<key>' | base64)
    3. Copy the aws_secret_access_key to "AWS_SECRET" (use echo -n '<key>' | base64)
3. Create S3 buckets
    1. backend bucket - create the bucket
    2. Photos bucket - create the bucket
    3. Photos bucket - allow public access and Add the correct policy (see how in the comment inside infra/modules/s3/main.tf)
    4. Photos bucket - upload the photos
4. in infra folder: ti -> tp -> ta
5. Manually Verify runner runs with the new github Runner's SSH key
6. Give the EC2 of the k8s_cluster security IAM of "labInstanceProfile"
7. Change IAM "LabRole" permissions to full admin to have access to s3 resources
8. Run "Install Kind Cluster on EC2" with the IP of the K8S_cluster
9. Run CD


