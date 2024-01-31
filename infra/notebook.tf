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

# If you happen to not be signed-in to AWS Console, use the following command
# in your Terminal. This long URL will let you enter the notebook.
# aws sagemaker create-presigned-notebook-instance-url --notebook-instance-name SageMakerNotebook --region us-east-2 --query AuthorizedUrl --output text
