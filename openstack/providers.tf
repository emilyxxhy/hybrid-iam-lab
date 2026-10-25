terraform {
  required_version = ">= 1.10.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.53.0"
    }
  }
}

# Reads ~/.config/openstack/clouds.yaml -> the "openstack" entry
provider "openstack" {
  cloud = "openstack"
}
