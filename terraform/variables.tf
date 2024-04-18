variable "credentials" {
  description = "My credentials"
}

variable "project_id" {
  description = "GCP Project"
}

variable "location" {
  description = "Project location"
  default     = "US"
}

variable "staging_dataset_name" {
  description = "My bq dataset name"
  default     = "brazilian_reits_staging"
}

variable "prod_dataset_name" {
  description = "My bq dataset name"
  default     = "brazilian_reits"
}

variable "gcs_storage_class" {
  description = "Bucket storage class"
  default     = "STANDARD"
}

variable "gcs_bucket_name" {
  description = "My storage bucket name"
  default     = "brazilian-reits-bucket"
}