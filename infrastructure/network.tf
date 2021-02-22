resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.application} ${var.role}"
    application = var.application
    role = var.role
  }
}


resource "aws_security_group" "instance" {
  name = "${var.application}-${var.role}-instance-sg"
  description = "Security group for the main ${var.application}-${var.role} server."
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${ var.application } ${ var.role } - Instance"
    application = var.application
    role = var.role
  }

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [
      var.operations_ip_address
    ]
  }

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_security_group" "database" {
  name = "${var.application}-${var.role}-database-sg"
  description = "Security group for the ${var.application} ${var.role} database server."
  tags = {
    Name = "${var.application} ${var.role} database"
    application = var.application
    role = var.role
  }

  vpc_id = aws_vpc.vpc.id

  ingress {
    cidr_blocks = [
      "10.0.0.0/16",
      var.operations_ip_address,
    ]
    to_port = 3306
    from_port = 3306
    protocol = "tcp"
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_subnet" "subnet_a" {
  vpc_id = aws_vpc.vpc.id
  cidr_block = "10.0.0.0/24"
  availability_zone_id = data.aws_availability_zones.available.zone_ids[ 0 ]

  tags = {
    Name = "${var.application} ${var.role} subnet for ${ data.aws_availability_zones.available.zone_ids[ 0 ] }"
    application = var.application
    role = var.role
  }
}


resource "aws_subnet" "subnet_b" {
  vpc_id = aws_vpc.vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone_id = data.aws_availability_zones.available.zone_ids[ 1 ]

  tags = {
    Name = "${var.application} ${var.role} subnet for ${ data.aws_availability_zones.available.zone_ids[ 1 ] }"
    application = var.application
    role = var.role
  }
}


resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "${var.application} ${var.role}"
    application = var.application
    role = var.role
  }
}


resource "aws_route" "internet_gateway_route" {
  route_table_id = aws_vpc.vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.internet_gateway.id
}
