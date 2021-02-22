resource "aws_db_subnet_group" "db_subnet_group" {
  name = "${var.application}-${var.role}"
  subnet_ids = [
    aws_subnet.subnet_a.id,
    aws_subnet.subnet_b.id,
  ]

  tags = {
    Name = "${var.application} ${var.role}"
    application = var.application
    role = var.role
  }
}


resource "aws_db_instance" "database" {
  identifier = "${var.application}-${var.role}"
  allocated_storage = 20
  storage_type = "gp2"
  engine = "mysql"
  engine_version = "5.7"
  instance_class = "db.t2.micro"
  name = "ginkgobioworks"
  username = "ginkgobioworks"
  password = "ginkgobioworks"
  parameter_group_name = "default.mysql5.7"
  db_subnet_group_name = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids = [
    aws_security_group.database.id,
  ]
  publicly_accessible = true
  skip_final_snapshot = var.skip_final_snapshot
  deletion_protection = var.database_deletion_protection

  tags = {
    Name = "${var.application} ${var.role}"
    application = var.application
    role = var.role
  }
}
