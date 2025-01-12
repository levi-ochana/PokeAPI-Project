# output
output "backend-server_eip" {
  value = aws_eip.backend-server_eip.public_ip
}

output "web-server_eip" {
  value = aws_eip.web-server_eip.public_ip
}

