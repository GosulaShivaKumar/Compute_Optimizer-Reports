import boto3
import time
from datetime import date

today = date.today()
get_date = today.strftime("%d-%m-%Y-%H:%M:%S")

def export_ec2_instance_recommendations(account):
    client = boto3.client('compute-optimizer')
    response = client.export_ec2_instance_recommendations(
        accountIds=[account],
        s3DestinationConfig={
            'bucket': 'compute-optimizer-organizational-report',
            'keyPrefix': account+'/'+get_date+'/EC2'
        },
    )
    return response['jobId']

def export_ecs_service_recommendations(account):
    client = boto3.client('compute-optimizer')
    response = client.export_ecs_instance_recommendations(
        accountIds=[account],
        s3DestinationConfig={
            'bucket': 'compute-optimizer-organizational-report',
            'keyPrefix': account+'/'+get_date+'/ECS'
        },
    )
    return response['jobId']

def export_lambda_function_recommendations(account):
    client = boto3.client('compute-optimizer')
    response = client.export_lambda_function_recommendations(
        accountIds=[account],
        s3DestinationConfig={
            'bucket': 'compute-optimizer-organizational-report',
            'keyPrefix': account+'/'+get_date+'/Lambda'
        },
    )
    return response['jobId']

def export_ebs_volume_recommendations(account):
    client = boto3.client('compute-optimizer')
    response = client.export_ebs_volume_recommendations(
        accountIds=[account],
        s3DestinationConfig={
            'bucket': 'compute-optimizer-organizational-report',
            'keyPrefix': account+'/'+get_date+'/EBS'
        },
    )
    return response['jobId']

def export_auto_scaling_group_recommendations(account):
    client = boto3.client('compute-optimizer')
    response = client.export_auto_scaling_group_recommendations(
        accountIds=[account],
        s3DestinationConfig={
            'bucket': 'compute-optimizer-organizational-report',
            'keyPrefix': account+'/'+get_date+'/ASG'
        },
    )
    return response['jobId']

def lambda_handler(event, context):
    try:
        account_list = ["119877415835"]
        command_to_export = {
            'export_ec2_instance_recommendations': export_ec2_instance_recommendations,
            'export_ecs_service_recommendations': export_ecs_service_recommendations,
            'export_lambda_function_recommendations': export_lambda_function_recommendations,
            'export_ebs_volume_recommendations': export_ebs_volume_recommendations,
            'export_auto_scaling_group_recommendations': export_auto_scaling_group_recommendations,
        }

        for account in account_list:
            for command, export_func in command_to_export.items():
                job_id = export_func(account)
                loop_time = 1
                loop_status = True
                while loop_status:
                    client = boto3.client('compute-optimizer')
                    job_status = client.describe_recommendation_export_jobs(
                        jobIds=[job_id]
                    )

                    if job_status['recommendationExportJobs'][0]['status'] == 'Failed':
                        print(f'The job {job_id} failed')
                        job_status = "Failed"
                        loop_status = False

                    elif job_status['recommendationExportJobs'][0]['status'] == "Complete":
                        print(f"Job {job_id} is Complete.")
                        job_status = "Success"
                        loop_status = False

                    else:
                        print(f"Job {job_id} is still running. Waiting for 90 seconds...")
                        time.sleep(90)
                        loop_time += 1
                        loop_limit = 10

                        if loop_time >= loop_limit:
                            print("Job didn't complete after 10 minutes timeout.")
                            job_status = "TimedOut"

    except Exception as e:
        print('This is e', str(e))
        print(f"Error: {str(e)}")
        if 'LimitExceededException' in str(e):
            print('There is already a job running')
