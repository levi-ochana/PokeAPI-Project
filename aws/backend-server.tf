# Create a EC2 Instance for backend-server
resource "aws_instance" "backend-server" {
  ami           = "ami-055e3d4f0bbeb5878"  # Amazon Linux 2 AMI ID
  instance_type = var.instance_type  # Use a t2.micro instance for the free tier
  key_name = data.aws_key_pair.poke_key_pair.key_name
  subnet_id     = aws_subnet.poke_subnet.id
  security_groups = [aws_security_group.poke_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "backend-server"
  }
# User data script to set up the EC2 instance
  user_data = <<-EOF
              #!/bin/bash

              # Update the system and install Docker
              sudo yum update -y  # Update packages
              sudo yum install -y docker  # Install Docker
              sudo service docker start  # Start Docker service
              sudo usermod -a -G docker ec2-user  # Add user to Docker group
              EOF
}

