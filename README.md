# Hybrid IAM Lab
Terraform config for an identity lab in Azure Entra ID (users, groups, RBAC).
Later: on-prem AD synced via Entra Connect.

## Run
cd terraform
az login
cp terraform.tfvars.example terraform.tfvars   # then edit it
terraform init && terraform plan
