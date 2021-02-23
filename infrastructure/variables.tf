variable "ami" {}
variable "application" {}
variable "database_deletion_protection" {}
variable "database_password" {}
variable "database_user" {}
variable "fqdn" {}
variable "instance_type" {}
variable "key_name" {}
variable "operations_ip_address" {}
variable "role" {}
variable "skip_final_snapshot" {}
variable "ssh_key_path" {}
variable "zone_id" {}


variable "tls_private_key" {
  default = "key.pem"
}

variable "tls_certificate_chain" {
  default = "chain.pem"
}
