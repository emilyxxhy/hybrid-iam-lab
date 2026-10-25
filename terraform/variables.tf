variable "domain" {
  description = "Your Entra tenant domain, e.g. yourname.onmicrosoft.com"
  type        = string
}

variable "lab_users" {
  description = "Lab users to create, keyed by username"
  type = map(object({
    display_name = string
    department   = string
  }))
}
