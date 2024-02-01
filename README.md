Some machine learning experiments

Deploy the infrastructure with these command:
```bash
cd infra/
terraform init
terraform apply
```

To get a URL with token to Jupyter notebook without the need to log in to AWS,
use the following command and paste the output in your browser location bar:
```bash
aws sagemaker create-presigned-notebook-instance-url\
 --notebook-instance-name SageMakerNotebook\
 --region us-east-2\
 --query AuthorizedUrl\
 --output text
```

To save money and not destroy everything, just terminate the notebook:

```bash
terraform destroy -target aws_sagemaker_notebook_instance.SageMakerNotebook
```