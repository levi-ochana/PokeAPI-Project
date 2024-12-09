

provider "aws" {
  region = var.region  # Use the region variable
}

# Create a VPC (Virtual Private Cloud)
resource "aws_vpc" "poke_vpc" {
  cidr_block = var.vpc_cidr_block  # Use the VPC CIDR block variable
}

# Create a subnet in the VPC
resource "aws_subnet" "poke_subnet" {
  vpc_id            = aws_vpc.poke_vpc.id
  cidr_block        = var.subnet_cidr_block  # Use the subnet CIDR block variable
  availability_zone = var.availability_zone  # Use the availability zone variable
}


# Use an existing Key Pair "vockey" 
data "aws_key_pair" "poke_key_pair" {
  key_name = "vockey"
}

# Create a Security Group
resource "aws_security_group" "poke_sg" {
  vpc_id = aws_vpc.poke_vpc.id

  # Allow SSH access to EC2 instances (port 22)
  ingress {
    from_port   = var.ssh_port  # Use the SSH port variable
    to_port     = var.ssh_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow Flask API access (port 5000)
  ingress {
    from_port   = var.flask_api_port  # Use the Flask API port variable
    to_port     = var.flask_api_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTP web app access (port 80)
  ingress {
    from_port   = var.http_port  # Use the HTTP port variable
    to_port     = var.http_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow access to game app (port 8080)
  ingress {
    from_port   = var.game_app_port  # Port 8080 for the game app
    to_port     = var.game_app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow access from anywhere
  }

# Allow access to MongoDB (port 27017)
ingress {
  from_port   = var.MongoDB_port
  to_port     = var.MongoDB_port
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"] 
}


  # Allow all outgoing traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# create Internet Gateway 
resource "aws_internet_gateway" "poke_igw" {
  vpc_id = aws_vpc.poke_vpc.id  
  tags = {
    Name = "PokeAPI-IGW"
  }
}

# create Route Table
resource "aws_route_table" "poke_route_table" {
  vpc_id = aws_vpc.poke_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.poke_igw.id  
  }

  tags = {
    Name = "PokeAPI-RouteTable"
  }
}

resource "aws_route_table_association" "poke_route_table_association" {
  subnet_id      = aws_subnet.poke_subnet.id
  route_table_id = aws_route_table.poke_route_table.id
}




# Allocate an Elastic IP for the backend EC2 instance
resource "aws_eip" "poke_backend_eip" {
  instance = aws_instance.backend_instance.id  # Attach the EIP to your EC2 instance
  domain      = "vpc"
}

# Allocate an Elastic IP for the game instance EC2 instance
resource "aws_eip" "poke_game_eip" {
  instance = aws_instance.game_instance.id  # Attach the EIP to your game EC2 instance
  domain      = "vpc"
}

# output
output "poke_backend_eip" {
  value = aws_eip.poke_backend_eip.public_ip
}

output "poke_game_eip" {
  value = aws_eip.poke_game_eip.public_ip
}

