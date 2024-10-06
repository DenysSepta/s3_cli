import boto3
import click
import re
import os
import logging
import tqdm
import time
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError, EndpointConnectionError

logging.basicConfig(level=logging.WARNING)

# Initialize the S3 client using environment variables
def get_s3_client():
    try:
        return boto3.client('s3')
    except (NoCredentialsError, PartialCredentialsError) as e:
        click.echo(f"Error: Invalid AWS credentials - {str(e)}")
        raise

# Retry logic for transient errors
def retry_with_backoff(func, retries=3, delay=1):
    for i in range(retries):
        try:
            return func()
        except EndpointConnectionError as e:
            if i < retries - 1:
                time.sleep(delay * 2 ** i)  # Exponential backoff
            else:
                click.echo(f"Error: Unable to connect to AWS after {retries} attempts.")
                raise e

# Command to list all files in the S3 bucket within a specified prefix
@click.command(help="List all files in the S3 bucket under the specified prefix.")
@click.option('--bucket', default='developer-task', help="S3 bucket name")
@click.option('--prefix', default='x-wing/', help="S3 prefix (directory) in the bucket")
@click.option('--output-format', type=click.Choice(['json', 'text']), default='text', help="Output format")
def list_files(bucket, prefix, output_format):
    try:
        s3 = get_s3_client()
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

        files = []
        for page in pages:
            for obj in page.get('Contents', []):
                files.append(obj['Key'])

        if output_format == 'json':
            click.echo(files)
        else:
            for file in files:
                click.echo(file)

        if not files:
            click.echo("No files found.")
    except ClientError as e:
        click.echo(f"Error accessing bucket: {str(e)}")
    except EndpointConnectionError:
        click.echo("Error: Unable to connect to AWS. Check your network.")

# Command to upload a local file to a defined S3 location with a progress bar
@click.command(help="Upload a file to S3 with progress bar.")
@click.argument('local_file')  # The path of the local file to upload
@click.argument('s3_key')      # The destination S3 key (path within the bucket)
@click.option('--bucket', default='developer-task', help="S3 bucket name")
def upload_file(local_file, s3_key, bucket):
    if not os.path.exists(local_file):
        click.echo(f"Error: File {local_file} not found.")
        return

    try:
        s3 = get_s3_client()

        with tqdm.tqdm(total=os.path.getsize(local_file), unit='B', unit_scale=True) as pbar:
            s3.upload_file(local_file, bucket, s3_key, Callback=lambda bytes_transferred: pbar.update(bytes_transferred))
        
        click.echo(f"File {local_file} uploaded to {bucket}/{s3_key}")
    except FileNotFoundError:
        click.echo(f"Error: Local file {local_file} does not exist.")
    except ClientError as e:
        click.echo(f"Error uploading file: {str(e)}")
    except EndpointConnectionError:
        click.echo("Error: Unable to connect to AWS. Check your network.")

# Command to list files in the bucket matching a regex pattern
@click.command(help="List files in S3 that match a regex pattern.")
@click.argument('regex_pattern')  # The regex pattern to filter files
@click.option('--bucket', default='developer-task', help="S3 bucket name")
@click.option('--prefix', default='x-wing/', help="S3 prefix (directory) in the bucket")
def list_filtered_files(regex_pattern, bucket, prefix):
    try:
        pattern = re.compile(regex_pattern)
    except re.error as e:
        click.echo(f"Error: Invalid regex pattern - {str(e)}")
        return

    try:
        s3 = get_s3_client()
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

        files = []
        for page in pages:
            for obj in page.get('Contents', []):
                if pattern.match(obj['Key']):
                    files.append(obj['Key'])

        if files:
            click.echo(f"Files matching pattern '{regex_pattern}':")
            for file in files:
                click.echo(file)
        else:
            click.echo("No files matching the pattern were found.")
    except ClientError as e:
        click.echo(f"Error accessing bucket: {str(e)}")
    except EndpointConnectionError:
        click.echo("Error: Unable to connect to AWS. Check your network.")

# Command to delete all files matching a regex pattern with dry-run option
@click.command(help="Delete files in S3 that match a regex pattern.")
@click.argument('regex_pattern')  # The regex pattern to delete matching files
@click.option('--bucket', default='developer-task', help="S3 bucket name")
@click.option('--prefix', default='x-wing/', help="S3 prefix (directory) in the bucket")
@click.option('--dry-run', is_flag=True, help="Show what would be deleted without actually deleting.")
def delete_filtered_files(regex_pattern, bucket, prefix, dry_run):
    try:
        pattern = re.compile(regex_pattern)
    except re.error as e:
        click.echo(f"Error: Invalid regex pattern - {str(e)}")
        return

    try:
        s3 = get_s3_client()
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

        files_to_delete = []
        for page in pages:
            for obj in page.get('Contents', []):
                if pattern.match(obj['Key']):
                    files_to_delete.append(obj['Key'])

        if not files_to_delete:
            click.echo("No files matching the pattern were found.")
            return

        if dry_run:
            click.echo(f"Dry run: The following files would be deleted:")
            for file in files_to_delete:
                click.echo(file)
        else:
            click.echo(f"Deleting files matching pattern '{regex_pattern}':")
            for file in files_to_delete:
                s3.delete_object(Bucket=bucket, Key=file)
                click.echo(f"Deleted {file}")
    except ClientError as e:
        click.echo(f"Error deleting files: {str(e)}")
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
