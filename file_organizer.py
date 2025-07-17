import os
import shutil

class FileOrganizer:
    """
    A class to organize files in a source directory into subdirectories
    based on their file extensions within an organized directory.
    """

    def __init__(self, source_dir="source", organized_dir="organized"):
        """
        Initializes the FileOrganizer with source and organized directories.

        Args:
            source_dir (str): The path to the directory containing unorganized files.
                              Defaults to 'source'.
            organized_dir (str): The path to the directory where files will be organized.
                                 Subdirectories (e.g., 'organized/txt') will be created here.
                                 Defaults to 'organized'.
        """
        self.source_dir = source_dir
        self.organized_dir = organized_dir
        self._create_base_directories()

    def _create_base_directories(self):
        """
        Ensures that the source and organized base directories exist.
        If they don't, they are created.
        """
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.organized_dir, exist_ok=True)
        print(f"Ensured '{self.source_dir}' and '{self.organized_dir}' directories exist.")

    def organize_files(self):
        """
        Reads files from the source directory, creates extension-based subdirectories
        in the organized directory, and moves files accordingly.
        """
        print(f"Starting file organization from '{self.source_dir}' to '{self.organized_dir}'...")
        files_organized_count = 0

        # Iterate over all items in the source directory
        for filename in os.listdir(self.source_dir):
            source_filepath = os.path.join(self.source_dir, filename)

            # Skip directories, only process files
            if os.path.isfile(source_filepath):
                # Get the file extension (e.g., '.txt', '.png')
                # os.path.splitext returns a tuple: (root, ext)
                _, file_extension = os.path.splitext(filename)

                # Remove the leading dot from the extension and convert to lowercase
                # If no extension (e.g., 'README'), it will be an empty string,
                # so we default to 'no_extension'
                extension_folder_name = file_extension[1:].lower() if file_extension else "no_extension"

                # Define the target directory for this extension
                target_extension_dir = os.path.join(self.organized_dir, extension_folder_name)

                # Create the extension-specific directory if it doesn't exist
                os.makedirs(target_extension_dir, exist_ok=True)

                # Define the destination path for the file
                destination_filepath = os.path.join(target_extension_dir, filename)

                try:
                    # Move the file from source to the organized directory
                    shutil.move(source_filepath, destination_filepath)
                    print(f"Moved '{filename}' to '{target_extension_dir}/'")
                    files_organized_count += 1
                except Exception as e:
                    print(f"Error moving '{filename}': {e}")
            else:
                print(f"Skipping directory or special file: '{filename}'")

        print(f"File organization complete. {files_organized_count} files organized.")



    