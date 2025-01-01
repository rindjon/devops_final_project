resource "aws_s3_bucket" "main" {
  bucket = var.bucket_name

  tags = {
    Name = var.name
  }

  # Configure public access block settings
  # block_public_acls = false
  # block_public_policy = false
  # ignore_public_acls = false
  # restrict_public_buckets = false

}

# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Sid": "PublicReadGetObject",
#             "Effect": "Allow",
#             "Principal": "*",
#             "Action": "s3:GetObject",
#             "Resource": "arn:aws:s3:::devops-final-project-photos/*"
#         }
#     ]
# }

resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.aws_s3_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.main.arn
}

output "bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.main.bucket
}