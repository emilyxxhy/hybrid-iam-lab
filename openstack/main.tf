resource "openstack_networking_secgroup_v2" "dc" {
  name        = "lab-dc-sg"
  description = "RDP + ping to the lab DC"
}

resource "openstack_networking_secgroup_rule_v2" "rdp" {
  security_group_id = openstack_networking_secgroup_v2.dc.id
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 3389
  port_range_max    = 3389
  remote_ip_prefix  = "0.0.0.0/0"
}

resource "openstack_networking_secgroup_rule_v2" "icmp" {
  security_group_id = openstack_networking_secgroup_v2.dc.id
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "icmp"
  remote_ip_prefix  = "0.0.0.0/0"
}

resource "openstack_compute_instance_v2" "dc" {
  name            = "lab-dc01"
  image_name      = "Windows Server 2022 Standard"
  flavor_name     = "m1.xlarge"
  security_groups = [openstack_networking_secgroup_v2.dc.name]

  network {
    name = "External Network"
  }
}