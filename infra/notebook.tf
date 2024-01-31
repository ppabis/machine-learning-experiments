resource "aws_sagemaker_notebook_instance" "SageMakerNotebook" {
  role_arn               = aws_iam_role.sagemaker.arn
  instance_type          = "ml.t3.medium"
  name                   = "SageMakerNotebook"
  direct_internet_access = "Enabled"
  root_access            = "Enabled"
}

output "Jupyter" {
  value = "https://${aws_sagemaker_notebook_instance.SageMakerNotebook.url}"
}
