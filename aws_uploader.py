import os
import boto3
from botocore.exceptions import ClientError

class AWSUploader:
    """
    A class to upload organized files from a local directory to an AWS S3 bucket.
    """

    def __init__(self, organized_dir="organized", bucket_name=None, region_name="us-east-1"):
        """
        Initializes the AWSUploader with the organized directory, S3 bucket name, and AWS region.

        Args:
            organized_dir (str): The local directory containing the organized files.
                                 Defaults to 'organized'.
            bucket_name (str): The name of the S3 bucket to upload files to.
                               This is a mandatory argument and must be provided.
            region_name (str): The AWS region for the S3 bucket. Defaults to 'us-east-1'.
        """
        if bucket_name is None:
            raise ValueError("S3 bucket_name must be provided.")

        self.organized_dir = organized_dir
        self.bucket_name = bucket_name
        self.region_name = region_name

        # Initialize the S3 client
        try:
            self.s3_client = boto3.client('s3', region_name=self.region_name)
            print(f"AWS S3 client initialized for region: {self.region_name}")
        except ClientError as e:
            print(f"Error initializing S3 client: {e}")
            self.s3_client = None # Set to None if initialization fails

    def _upload_file_to_s3(self, file_path, s3_object_key):
        """
        Uploads a single file to the specified S3 bucket.

        Args:
            file_path (str): The full local path to the file to upload.
            s3_object_key (str): The desired key (path) for the object in S3.

        Returns:
            bool: True if the file was uploaded successfully, False otherwise.
        """
        if self.s3_client is None:
            print("S3 client not initialized. Cannot upload file.")
            return False

        try:
            self.s3_client.upload_file(file_path, self.bucket_name, s3_object_key)
            print(f"Successfully uploaded '{file_path}' to s3://{self.bucket_name}/{s3_object_key}")
            return True
        except ClientError as e:
            print(f"Error uploading '{file_path}' to S3: {e}")
            return False

    def upload_organized_files(self):
        """
        Traverses the organized directory and uploads all files to the S3 bucket,
        preserving the directory structure within the bucket.
        """
        if not os.path.exists(self.organized_dir):
            print(f"Error: Organized directory '{self.organized_dir}' does not exist.")
            return

        if self.s3_client is None:
            print("S3 client not initialized. Aborting upload.")
            return

        print(f"Starting upload of organized files from '{self.organized_dir}' to S3 bucket '{self.bucket_name}'...")
        files_uploaded_count = 0

        # Walk through the organized directory
        for root, _, files in os.walk(self.organized_dir):
            for filename in files:
                local_file_path = os.path.join(root, filename)

                # Construct the S3 object key, preserving the folder structure
                # Example: organized/txt/document.txt -> txt/document.txt
                # os.path.relpath calculates the path relative to organized_dir
                s3_object_key = os.path.relpath(local_file_path, self.organized_dir)
                s3_object_key = s3_object_key.replace(os.sep, '/') # Ensure forward slashes for S3 keys

                if self._upload_file_to_s3(local_file_path, s3_object_key):
                    files_uploaded_count += 1

        print(f"File upload complete. {files_uploaded_count} files uploaded to S3.")

# Example usage (for testing purposes, will be called from main.py)
if __name__ == "__main__":
    # IMPORTANT: Replace 'your-unique-s3-bucket-name' with an actual S3 bucket name
    # that you have created and have access to.
    # Also, ensure your AWS credentials are configured (e.g., via AWS CLI, environment variables, or IAM role).
    # For local testing, you might use:
    # aws configure
    # and provide your Access Key ID and Secret Access Key.
    try:
        uploader = AWSUploader(bucket_name="your-unique-s3-bucket-name-here", region_name="us-east-1")
        # To test, you would typically run file_organizer first to populate 'organized/'
        # Then, you would call:
        # uploader.upload_organized_files()
        print("\nTo test this script:")
        print("1. Ensure you have an S3 bucket named 'your-unique-s3-bucket-name-here' (or change it).")
        print("2. Make sure your AWS credentials are configured.")
        print("3. Run file_organizer.py first to populate the 'organized/' directory.")
        print("4. Then uncomment and run 'uploader.upload_organized_files()' below.")
        # uploader.upload_organized_files()
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
