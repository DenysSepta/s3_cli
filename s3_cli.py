import boto3
import click
import re
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError, EndpointConnectionError
import logging

logging.basicConfig(level=logging.WARNING)

# Initialize the S3 client using the provided AWS credentials
def get_s3_client():
    try:
        return boto3.client(
            's3',
            aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        click.echo(f"Error: Invalid AWS credentials - {str(e)}")
        raise

# Command to list all files in the S3 bucket within the "x-wing" prefix
@click.command()
def list_files():
    try:
        s3 = get_s3_client()
        bucket_name = 'developer-task'
        prefix = 'x-wing/'

        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if 'Contents' in response:
            click.echo("Listing all files:")
            for obj in response['Contents']:
                click.echo(obj['Key'])
        else:
            click.echo("No files found.")
    except ClientError as e:
        click.echo(f"Error accessing bucket: {str(e)}")
    except EndpointConnectionError:
        click.echo("Error: Unable to connect to AWS. Check your network.")

# Command to upload a local file to a defined S3 location
@click.command()
@click.argument('local_file')  # The path of the local file to upload
@click.argument('s3_key')      # The destination S3 key (path within the bucket)
def upload_file(local_file, s3_key):
    if not os.path.exists(local_file):
        click.echo(f"Error: File {local_file} not found.")
        return

    try:
        s3 = get_s3_client()
        bucket_name = 'developer-task'

        s3.upload_file(local_file, bucket_name, s3_key)
        click.echo(f"File {local_file} uploaded to {s3_key}")
    except FileNotFoundError:
        click.echo(f"Error: Local file {local_file} does not exist.")
    except ClientError as e:
        click.echo(f"Error uploading file: {str(e)}")
    except EndpointConnectionError:
        click.echo("Error: Unable to connect to AWS. Check your network.")

# Command to list files in the bucket matching a regex pattern
@click.command()
@click.argument('regex_pattern')  # The regex pattern to filter files
def list_filtered_files(regex_pattern):
    try:
        pattern = re.compile(regex_pattern)
    except re.error as e:
        click.echo(f"Error: Invalid regex pattern - {str(e)}")
        return

    try:
        s3 = get_s3_client()
        bucket_name = 'developer-task'
        prefix = 'x-wing/'

        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if 'Contents' in response:
            click.echo(f"Files matching pattern '{regex_pattern}':")
            for obj in response['Contents']:
                if pattern.match(obj['Key']):
                    click.echo(obj['Key'])
        else:
            click.echo("No files found.")
    except ClientError as e:
        click.echo(f"Error accessing bucket: {str(e)}")
    except EndpointConnectionError:
        click.echo("Error: Unable to connect to AWS. Check your network.")

# Command to delete all files matching a regex pattern
@click.command()
@click.argument('regex_pattern')  # The regex pattern to delete matching files
def delete_filtered_files(regex_pattern):
    try:
        pattern = re.compile(regex_pattern)
    except re.error as e:
        click.echo(f"Error: Invalid regex pattern - {str(e)}")
        return

    try:
        s3 = get_s3_client()
        bucket_name = 'developer-task'
        prefix = 'x-wing/'

        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if 'Contents' in response:
            click.echo(f"Deleting files matching pattern '{regex_pattern}':")
            for obj in response['Contents']:
                if pattern.match(obj['Key']):
                    try:
                        s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                        click.echo(f"Deleted {obj['Key']}")
                    except ClientError as e:
                        click.echo(f"Error deleting {obj['Key']}: {str(e)}")
        else:
            click.echo("No files matching the pattern were found.")
    except ClientError as e:
        click.echo(f"Error accessing bucket: {str(e)}")
    except EndpointConnectionError:
        click.echo("Error: Unable to connect to AWS. Check your network.")

# Grouping all the commands into a single CLI application
@click.group()
def cli():
    pass

cli.add_command(list_files)
cli.add_command(upload_file)
cli.add_command(list_filtered_files)
cli.add_command(delete_filtered_files)

# Entry point for the CLI application
if __name__ == '__main__':
    cli()
