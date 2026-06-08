import os
import shutil


def copy_static(source, destination):
    # Delete destination if it exists
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # Create fresh destination
    os.mkdir(destination)

    copy_recursive(source, destination)


def copy_recursive(source, destination):
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)

        else:
            print(f"Creating directory: {destination_path}")
            os.mkdir(destination_path)
            copy_recursive(source_path, destination_path)