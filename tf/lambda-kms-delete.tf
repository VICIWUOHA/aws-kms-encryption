# create execution role for lambda
resource "aws_iam_role" "lambda" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com",
        },
      }
    ],
  })
 
}

# Create policy for cloudwatch logs
resource "aws_iam_role_policy" "lambda_execution_role_kms_policy" {
  name = "lambda_execution_role_kms_policy"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "kms:ScheduleKeyDeletion",
        Resource = "*"
      }
    ]
  })

  depends_on = [ aws_iam_role.lambda ]
}

# create policy to allow lambda to write logs to cloudwatch
resource "aws_iam_role_policy" "lambda_execution_role_cloudwatch_logs_policy" {
  name = "lambda_execution_role_cloudwatch_logs_policy"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })

  depends_on = [aws_iam_role_policy.lambda_execution_role_kms_policy]
}


# create lambda
resource "aws_lambda_function" "delete_kms_key_lambda" {
  function_name    = "DeleteKMSKeyLambda"
  handler          = "deleteKMSLambda.lambda_handler"
  runtime          = "python3.8"
  role             = aws_iam_role.lambda.arn
  filename         = "deletion_lambda.zip"  # ZIP file containing your Lambda function code

  
  environment {
    variables = {
      KMS_KEY_ID = var.kms_key_id  # Replace with the actual KMS key ID
    }
  }
  depends_on = [aws_iam_role_policy.lambda_execution_role_cloudwatch_logs_policy]
}

# resource for invoking lambda
resource "null_resource" "invoke_lambda" {
  depends_on = [aws_lambda_function.delete_kms_key_lambda]

  provisioner "local-exec" {
    command = <<EOT
      aws lambda invoke \
        --function-name ${aws_lambda_function.delete_kms_key_lambda.function_name} \
        --log-type Tail \
        output.json
    EOT
  }
}
