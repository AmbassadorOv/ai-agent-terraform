packer {
  required_plugins {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.0.0"
    }
  }
}

source "amazon-ebs" "ubuntu" {
  ami_name      = "ubuntu-fastapi-{{timestamp}}"
  instance_type = "t2.micro" 
  region        = "us-east-1" 
  source_ami    = "ami-0c55b159cbfafe1f0" # Ubuntu 20.04 LTS
  ssh_username  = "ubuntu"
  
  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y python3 python3-pip git",
      "pip3 install fastapi uvicorn",
      "git clone https://github.com/bmaelum/fastapi-hello-world.git /app",
      "sudo chown -R ubuntu:ubuntu /app",
      "sudo tee /etc/systemd/system/fastapi.service <<EOF",
      "[Unit]",
      "Description=FastAPI Application",
      "After=network.target",
      "",
      "[Service]",
      "User=ubuntu",
      "Group=ubuntu",
      "WorkingDirectory=/app/fastapi-hello-world",
      "ExecStart=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000",
      "Restart=always",
      "",
      "[Install]",
      "WantedBy=multi-user.target",
      "EOF",
      "sudo systemctl daemon-reload",
      "sudo systemctl enable fastapi.service"
    ]
  }
}

build {
  sources = ["source.amazon-ebs.ubuntu"]
}
