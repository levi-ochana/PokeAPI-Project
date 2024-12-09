variable "region" {
  description = "AWS Region"
  default     = "us-west-2"  
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "subnet_cidr_block" {
  description = "CIDR block for the subnet"
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "Availability zone for the subnet"
  default     = "us-west-2a"
}

variable "flask_api_port" {
  description = "Port for the Flask API"
  default     = 5000
}

variable "http_port" {
  description = "Port for HTTP access"
  default     = 80
}

variable "ssh_port" {
  description = "Port for SSH access"
  default     = 22
}

variable "game_app_port" {
  description = "Port for the game app"
  default     = 8080
}

variable "MongoDB_port" {
  description = "Port for the MongoDB port"
  default     = 27017
}


variable "instance_type" {
  description = "EC2 Instance Type"
  default     = "t2.micro"  # Use the free tier instance
}
