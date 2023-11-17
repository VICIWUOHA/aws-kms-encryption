variable "kms_key_id" {
  description = "KMS KEY ID TO BE DELETED"
  type        = string
  sensitive = true
  # default = "arn:aws:kms:us-east-1:your-kms-key-arn", this would help speed up your tf apply to avoid typing manually
  # avoid commiting such to git.
}
