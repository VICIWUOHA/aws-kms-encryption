## AWS Resource Mangement with Terraform (IAC)


The Terraform Scripts here spin up a lambda that deletes the KMS key and subsequently tears down  evrry resource created by terraform during the operation (including roles and policies) and the lambda function itself. For this to work, note that the AWS CLI and terraform have to be configured on your device.

## **Prerequisites:** 

_You must have both the Terraform CLI & the AWS CLI Installed locally._


## STEPS

1) cd into the **tf/** directory


2) Study the [deleteKMSLambda.py](/tf/deleteKMSLambda.py) file and compress it into a file named `deletion_lambda.zip` you can run the command below;

        zip deletion_lambda.zip deleteKMSLambda.py


3) Run your terraform commands. 

- Start with  `terraform init` , `terraform plan`, then `terraform apply`
At some point it should prompt you for your **kms_key_id** variable which you should provide. (this won't show when you paste it because it is sensitive.)
 You can also set the default value for this variable in your [variables.tf](/tf/variables.tf) file.


Output of Terraform Apply
==========

![Terrraform Apply](/assets/success_logs_local.png)

Output in Cloudwatch Logs
=======

![Cloudwatch Logs](/assets/cloudwatch-logs.png)


You should also notice a file named `output.json` in your tf directory if this was succesful.



## What Happens under the Hood

Terraform Makes the relevant API calls to AWS services on your behalf to create these resources and execute your lambda function.


## Tear down resources.

To delete the resources created by terraform, go ahead and run the command below;

    terraform destroy