variable "project_id" {
  type        = string
  description = "GCP Project ID"
  default     = "cicd-demo-468415"
}

variable "region" {
  type        = string
  description = "GCP region"
  default     = "europe-west2"
}

variable "environments" {
  type        = list(string)
  description = "List of environments"
  default     = ["dev", "uat", "prod"]
}

variable "folders" {
  type        = list(string)
  description = "Folder structure inside each bucket"
  default     = ["archive", "output", "raw", "staging", "temp"]
}

variable "prod_retention_days" {
  type        = number
  description = "Retention period for PROD bucket in days"
  default     = 30
}