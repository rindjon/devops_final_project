terraform {
  backend "s3" {
    bucket         = "ronrind-terraform-state"
    key            = "terraform/state/dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}
