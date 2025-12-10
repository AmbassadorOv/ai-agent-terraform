provider "aws" {
  region = var.region
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "instance_sg" {
  name        = "fastapi-instance-sg"
  description = "Security group for the EC2 instances"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [var.alb_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_launch_template" "fastapi_launch_template" {
  name_prefix   = "fastapi-"
  image_id      = var.ami_id
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.instance_sg.id]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "fastapi_asg" {
  name                = var.asg_name
  desired_capacity    = var.desired_capacity
  max_size            = var.max_size
  min_size            = var.min_size
  vpc_zone_identifier = data.aws_subnets.default.ids

  launch_template {
    id      = aws_launch_template.fastapi_launch_template.id
    version = "$Latest"
  }

  lifecycle {
    create_before_destroy = true
  }
}
