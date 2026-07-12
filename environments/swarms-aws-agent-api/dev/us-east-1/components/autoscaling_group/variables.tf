variable "ami_id" {
  description = "The ID of the AMI to use for the launch template."
  type        = string
}

variable "instance_type" {
  description = "The instance type to use for the launch template."
  type        = string
  default     = "t2.micro"
}

variable "asg_name" {
  description = "The name of the Auto Scaling Group."
  type        = string
  default     = "fastapi-asg"
}

variable "desired_capacity" {
  description = "The desired number of instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "alb_security_group_id" {
  description = "The ID of the security group for the Application Load Balancer."
  type        = string
}

variable "max_size" {
  description = "The maximum number of instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "min_size" {
  description = "The minimum number of instances in the Auto Scaling Group."
  type        = number
  default     = 1
}
