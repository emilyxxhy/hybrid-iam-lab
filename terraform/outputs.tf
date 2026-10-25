output "user_upns" {
  value = [for u in azuread_user.lab : u.user_principal_name]
}

output "it_admins_group_id" {
  value = azuread_group.it_admins.object_id
}
