import os
import shutil
import logging

logging.basicConfig(
    filename="file_sorter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def sort_files(selected_location):

    failed_folders = []

    failed_files = []

    extensions = {}

    count, skip = 0, 0

    for file in os.listdir(selected_location):
    
            if os.path.isfile(os.path.join(selected_location, file)):
    
                extension = os.path.splitext(file)[1]
    
                extension = extension.lstrip(".").upper()
    
                if extension == "":            
                    extension = "NO EXTENSION"
    
                try:
                    os.mkdir(os.path.join(selected_location, extension))
                    logging.info(f"Created folder '{extension}'")

                except FileExistsError:
                    logging.debug("Folder already exists.")
                    pass

                except OSError as e:
                    failed_folders.append((extension, str(e)))
                    logging.error(f"Failed to create folder '{extension}': {e}")
                    continue
    
                file_source = os.path.join(selected_location, file)
                file_destination = os.path.join(selected_location, extension, file)
    
                try:
                    shutil.move(file_source, file_destination)
    
                    count += 1
    
                    if extension not in extensions:
                        extensions[extension] = 1 
                    else:
                        extensions[extension] += 1

                    logging.info(f"Moved {file} to {file_destination}")

                except FileExistsError:
                    skip += 1
    
                except OSError as e:
                    failed_files.append((file, str(e)))
                    logging.error(f"Failed to move {file}: {e}")
                    continue

    return count, skip, extensions, failed_folders, failed_files