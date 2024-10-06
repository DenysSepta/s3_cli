
# S3 CLI Tool

This is a Python command-line interface (CLI) tool for interacting with AWS S3. It allows you to list, upload, filter, and delete files in an S3 bucket. The CLI is flexible with configurable bucket names and prefixes.

## Features

- **List Files**: List all files in a specific S3 prefix.
- **Upload File**: Upload a local file to a specified S3 path within the bucket.
- **List Filtered Files**: List files in the S3 bucket that match a specified regex pattern.
- **Delete Filtered Files**: Delete files in the S3 bucket that match a regex pattern, with optional dry run mode.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- AWS credentials (Access Key ID and Secret Access Key) set as environment variables:

### Setting AWS Credentials

#### Windows

Set the environment variables from the command prompt:

```cmd
setx AWS_ACCESS_KEY_ID "your_access_key_id"
setx AWS_SECRET_ACCESS_KEY "your_secret_access_key"
setx AWS_DEFAULT_REGION "your_region"
```

#### Linux/macOS

Add these lines to your `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
export AWS_ACCESS_KEY_ID='your_access_key_id'
export AWS_SECRET_ACCESS_KEY='your_secret_access_key'
export AWS_DEFAULT_REGION='your_region'
```

Then source the file to load the variables:

```bash
source ~/.bashrc
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

## Usage

This CLI tool has several commands that you can use for interacting with your S3 bucket.

### 1. List All Files

This command lists all files in the specified S3 bucket under a specific prefix:

```bash
python s3_cli.py list-files --bucket your-bucket-name --prefix your-prefix
```

Example:

```bash
python s3_cli.py list-files --bucket developer-task --prefix x-wing/
```

### 2. Upload a File

Uploads a local file to the specified S3 path within the bucket:

```bash
python s3_cli.py upload-file <local_file_path> <s3_key> --bucket your-bucket-name
```

Example:

```bash
python s3_cli.py upload-file ./test.txt x-wing/test.txt --bucket developer-task
```

### 3. List Files Matching a Regex Pattern

Lists files in the specified bucket and prefix that match a regex pattern:

```bash
python s3_cli.py list-filtered-files "<regex_pattern>" --bucket your-bucket-name --prefix your-prefix
```

Example (list all `.txt` files):

```bash
python s3_cli.py list-filtered-files ".*\.txt" --bucket developer-task --prefix x-wing/
```

### 4. Delete Files Matching a Regex Pattern

Delete files in the specified bucket and prefix that match a regex pattern. Use the `--dry-run` flag to simulate the deletion without actually deleting files:

```bash
python s3_cli.py delete-filtered-files "<regex_pattern>" --bucket your-bucket-name --prefix your-prefix --dry-run
```

To actually delete files (without dry run):

```bash
python s3_cli.py delete-filtered-files "<regex_pattern>" --bucket your-bucket-name --prefix your-prefix
```

Example (delete all `.txt` files in `x-wing/`):

```bash
python s3_cli.py delete-filtered-files ".*\.txt" --bucket developer-task --prefix x-wing/
```

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
- **Connection Issues**: The tool will notify you if there are connection issues, such as an incorrect region or network failure.

## License

This project is licensed under the MIT License.

## Contributing

Feel free to fork the project, submit issues, or make pull requests with improvements or new features!
