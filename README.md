
# S3 CLI Tool

This is a Python command-line interface (CLI) tool for interacting with AWS S3. It allows you to list, upload, filter, and delete files in an S3 bucket, specifically under the `x-wing/` prefix.

## Features

- **List Files**: List all files in the `x-wing/` prefix of the S3 bucket.
- **Upload File**: Upload a local file to a specified S3 path within the bucket.
- **List Filtered Files**: List files in the `x-wing/` prefix that match a specified regex pattern.
- **Delete Filtered Files**: Delete files in the `x-wing/` prefix that match a specified regex pattern.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- AWS credentials (Access Key ID and Secret Access Key)

## AWS Credentials Setup

Ensure your AWS credentials are set in the environment variables. These are required for accessing the S3 bucket. You can do this by setting the following variables:

### Linux/macOS

Add these lines to your `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
export AWS_ACCESS_KEY_ID='your_access_key_id'
export AWS_SECRET_ACCESS_KEY='your_secret_access_key'
```

Then source the file to load the variables:

```bash
source ~/.bashrc
```

### Windows

Set the environment variables from the command prompt:

```cmd
setx AWS_ACCESS_KEY_ID "your_access_key_id"
setx AWS_SECRET_ACCESS_KEY "your_secret_access_key"
```

After running these commands, restart your terminal or command prompt to apply the changes.

To check that the environment variables were set correctly, you can run:

```cmd
echo %AWS_ACCESS_KEY_ID%
echo %AWS_SECRET_ACCESS_KEY%
```

## Installation

### Clone the Repository

```bash
git clone https://github.com/DenysSepta/s3_cli.git
cd s3_cli
```

### Install Dependencies

You can install the necessary dependencies using `pip` and the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

The two required dependencies are:

- `boto3`: Python SDK for AWS
- `click`: Python package for creating CLI applications

## Usage

This CLI tool has several commands that you can use for interacting with your S3 bucket.

### List All Files

Lists all files under the `x-wing/` prefix in the `developer-task` S3 bucket.

```bash
python s3_cli.py list-files
```

### Upload a File

Uploads a local file to the `x-wing/` prefix in the S3 bucket.

```bash
python s3_cli.py upload-file <local_file_path> <s3_key>
```

**Example:**

```bash
python s3_cli.py upload-file ./test.txt x-wing/test.txt
```

### List Files with Regex Filter

Lists files in the `x-wing/` prefix that match a regex pattern.

```bash
python s3_cli.py list-filtered-files <regex_pattern>
```

**Example:**

```bash
python s3_cli.py list-filtered-files ".*\.txt"
```

This will list all files in the `x-wing/` prefix that end with `.txt`.

### Delete Files with Regex Filter

Deletes files in the `x-wing/` prefix that match a regex pattern.

```bash
python s3_cli.py delete-filtered-files <regex_pattern>
```

**Example:**

```bash
python s3_cli.py delete-filtered-files ".*\.log"
```

This will delete all files in the `x-wing/` prefix that end with `.log`.

## Project Structure

The project consists of the following files:

```
s3_cli/
├── .gitignore          # Specifies files to be ignored by Git
├── README.md           # Documentation
├── requirements.txt    # Python dependencies
├── s3_cli.py           # Python CLI script
```

## Error Handling

- **Invalid AWS Credentials**: The tool will alert you if the AWS credentials are missing or invalid.
- **File Not Found**: If a local file specified for upload is missing, it will report the error.
- **Invalid Regex**: If an invalid regex pattern is provided, the tool will notify you.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to fork the project, submit issues, or make pull requests with improvements or new features!
