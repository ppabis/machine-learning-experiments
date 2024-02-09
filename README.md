Some machine learning experiments

Refer to this blog post for more information:
https://pabis.eu/blog/2024-02-10-Lets-Play-Machine-Learning.html

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