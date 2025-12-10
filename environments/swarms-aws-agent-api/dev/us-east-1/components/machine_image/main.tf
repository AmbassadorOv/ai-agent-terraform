provider "aws" {
  region = var.region
}

data "aws_caller_identity" "current" {}

data "aws_ami" "fastapi_ami" {
  most_recent = true
  owners      = [data.aws_caller_identity.current.account_id]

  filter {
    name   = "name"
    values = ["ubuntu-fastapi-*"]
  }
}
