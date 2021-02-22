data "aws_availability_zones" "available" {
  state = "available"
}


resource "aws_instance" "ginkgo_bioworks_11x_engineering" {
  ami = var.ami
  instance_type = var.instance_type
  associate_public_ip_address = "true"
  key_name = var.key_name
  subnet_id = aws_subnet.subnet_a.id
  vpc_security_group_ids = [
    aws_security_group.instance.id,
  ]

  tags = {
    Name = "${ var.application } ${ var.role }"
    role = var.role
    application = var.application
  }
}


resource "aws_route53_record" "ginkgo_bioworks_11x_engineering" {
  allow_overwrite = true
  name = var.fqdn
  ttl = 60
  type = "A"
  zone_id = var.zone_id
  records = [
    aws_instance.ginkgo_bioworks_11x_engineering.public_ip,
  ]
}


resource "aws_route53_record" "www_ginkgo_bioworks_11x_engineering" {
  allow_overwrite = true
  name = "www.${var.fqdn}"
  ttl = 60
  type = "A"
  zone_id = var.zone_id
  records = [
    aws_instance.ginkgo_bioworks_11x_engineering.public_ip,
  ]
}
