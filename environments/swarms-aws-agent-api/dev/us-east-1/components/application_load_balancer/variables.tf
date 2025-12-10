variable "asg_name" {
  description = "The name of the Auto Scaling Group to attach the load balancer to."
  type        = string
}

variable "alb_name" {
  description = "The name of the Application Load Balancer."
  type        = string
  default     = "fastapi-alb"
}

variable "target_group_name" {
  description = "The name of the target group."
  type        = string
  default     = "fastapi-tg"
}

variable "region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}
