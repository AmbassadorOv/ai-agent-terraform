output "alb_dns_name" {
  description = "The DNS name of the Application Load Balancer"
  value       = aws_lb.fastapi_alb.dns_name
}

output "alb_security_group_id" {
  description = "The ID of the security group for the Application Load Balancer"
  value       = aws_security_group.alb_sg.id
}
