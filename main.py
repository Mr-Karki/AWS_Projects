import os
from file_organizer import FileOrganizer
from aws_uploader import AWSUploader
import sys

def main():
    """
    Main function to orchestrate the file organization and AWS S3 upload process.
    It initializes FileOrganizer and AWSUploader classes and calls their methods.
    """
    print("Starting the File Organizer with AWS Integration...")

    # --- Configuration ---
    # Define your source and organized directories
    source_directory = "source"
    organized_directory = "organized"

    # Define your S3 bucket name and region

    s3_bucket_name = os.environ.get("S3_BUCKET_NAME", "my-aws-file-organizer")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if s3_bucket_name == "your-unique-s3-bucket-name-here":
        print("\nWARNING: S3_BUCKET_NAME is still set to the default placeholder.")
        print("Please create an S3 bucket in your AWS account and update 's3_bucket_name' in main.py,")
        print("or set the S3_BUCKET_NAME environment variable before running.")
        print("Exiting without S3 upload.")
        sys.exit(1) # Exit the script if bucket name is not configured

    # --- Step 1: Organize Files Locally ---
    print("\n--- Step 1: Local File Organization ---")
    organizer = FileOrganizer(source_dir=source_directory, organized_dir=organized_directory)
    organizer.organize_files()

    # --- Step 2: Upload Organized Files to AWS S3 ---
    print("\n--- Step 2: Uploading Organized Files to AWS S3 ---")
    try:
        uploader = AWSUploader(organized_dir=organized_directory,
                               bucket_name=s3_bucket_name,
                               region_name=aws_region)
        uploader.upload_organized_files()
    except ValueError as ve:
        print(f"S3 Uploader Configuration Error: {ve}")
        print("Skipping S3 upload due to configuration error.")
    except Exception as e:
        print(f"An unexpected error occurred during S3 upload: {e}")
        print("Skipping S3 upload.")

    print("\nFile organization and AWS S3 upload process finished.")

if __name__ == "__main__":
    main()
