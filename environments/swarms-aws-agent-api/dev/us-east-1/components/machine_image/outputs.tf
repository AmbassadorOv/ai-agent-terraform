output "ami_id" {
  description = "The ID of the FastAPI AMI"
  value       = data.aws_ami.fastapi_ami.id
}
