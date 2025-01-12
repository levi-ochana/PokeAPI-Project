# Create an EC2 Instance for web-server Game 
resource "aws_instance" "web-server" {
  ami           = "ami-055e3d4f0bbeb5878"  # Amazon Linux 2 AMI ID
  instance_type = "t2.micro"  # Free tier instance type
  key_name = data.aws_key_pair.poke_key_pair.key_name
  subnet_id     = aws_subnet.poke_subnet.id
  security_groups = [aws_security_group.poke_sg.id]
  associate_public_ip_address = true


  tags = {
    Name = "web-server"
  }

  depends_on = [aws_instance.backend-server]

  # User data script to set up the EC2 instance
  user_data = <<-EOF
              #!/bin/bash
              # Update system packages
              sudo yum update -y

              # Install Git and Python3
              sudo yum install -y git python3 python3-pip

              # Clone the PokeAPI game from GitHub
              cd /home/ec2-user
              git clone https://github.com/levi-ochana/Poke_API

              # Navigate to the game directory
              cd Poke_API

              # Install Python dependencies
              sudo pip3 install requests

              # Run the game server
              nohup python3 game.py > game.log 2>&1 &
              EOF
}


