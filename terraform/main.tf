resource "random_password" "user" {
  for_each = var.lab_users
  length   = 20
  special  = true
}

resource "azuread_user" "lab" {
  for_each              = var.lab_users
  user_principal_name   = "${each.key}@${var.domain}"
  display_name          = each.value.display_name
  department            = each.value.department
  password              = random_password.user[each.key].result
  force_password_change = true
}

resource "azuread_group" "it_admins" {
  display_name     = "lab-it-admins"
  security_enabled = true
  members          = [for u in azuread_user.lab : u.object_id if u.department == "IT"]
}
