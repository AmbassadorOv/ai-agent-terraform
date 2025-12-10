output "asg_name" {
  description = "The name of the Auto Scaling Group"
  value       = aws_autoscaling_group.fastapi_asg.name
}
