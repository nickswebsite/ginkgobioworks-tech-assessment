resource "local_file" "inventory" {
  content = templatefile( "inventory.tmpl", {
    host = var.fqdn
    ssh_key_path = var.ssh_key_path
    variables = "infrastructure/ansible-variables.yml"
  } )
  filename = "inventory"
}


resource "local_file" "ansible_variables" {
  content = templatefile( "ansible-variables.tmpl.yml", {
    role = var.role

    public_dns = var.fqdn
    private_key = var.tls_private_key
    certificate = var.tls_certificate_chain

    database_host = aws_db_instance.database.address
    database_port = aws_db_instance.database.port
    database_name = aws_db_instance.database.name
    database_user = aws_db_instance.database.username
    database_password = aws_db_instance.database.password
  } )
  filename = "ansible-variables.yml"
}
