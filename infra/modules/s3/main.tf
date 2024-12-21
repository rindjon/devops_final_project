resource "aws_s3_bucket" "main" {
  bucket = var.bucket_name

  tags = {
    Name = var.name
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