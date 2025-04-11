import os

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION")


def is_running_on_aws():
    return AWS_REGION is not None


def get_params(param_names):
    ssm = boto3.client('ssm', region_name=AWS_REGION)
    params = {}

    for param_name in param_names:
        response = ssm.get_parameter(Name=param_name, WithDecryption=True)
        params[param_name] = response['Parameter']['Value']

    return params
