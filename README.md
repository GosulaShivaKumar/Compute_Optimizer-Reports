```markdown
# AWS Compute Optimizer Export Project using Lambda Functions in AWS

This Python project automates the export of AWS Compute Optimizer recommendations for various AWS resources like EC2 instances, ECS services, Lambda functions, EBS volumes, and Auto Scaling groups. The project uses the AWS SDK for Python (Boto3) to interact with AWS services, automating exports to an S3 bucket based on a provided account ID.

## Features

- Export recommendations for EC2, ECS, Lambda, EBS, and Auto Scaling groups.
- Automatically organize exports in an S3 bucket with a structured directory format.
- Handle export job statuses and retry logic.

## Prerequisites

Before you can run this script, you need to have:
- AWS CLI installed and configured with appropriate permissions.
- Python 3.x installed.
- Boto3 library installed. You can install it using pip:

```bash
pip install boto3
```

## Configuration

Update the `account_list` variable in the `lambda_handler` function to include the AWS account IDs you wish to generate reports for.

Ensure that the S3 bucket `compute-optimizer-organizational-report` exists and the executing AWS user has the necessary permissions to write to this bucket.

## Usage

To run this script, simply execute the Python file from your terminal:

```bash
python aws_optimizer_exports.py
```

The script will:
- Initiate export jobs for each specified service.
- Monitor the status of each job and provide updates on completion or failure.
- Handle timeouts and errors appropriately.

## Handling Export Jobs

The script includes functionality to handle different states of the job:
- If a job fails, it logs the failure.
- If a job completes successfully, it logs the completion.
- If a job does not complete within a predetermined timeout, it logs a timeout message.

## Error Handling

The script captures and logs exceptions, especially focusing on service limit exceptions, allowing for better manageability in scenarios where multiple exports are initiated simultaneously.

