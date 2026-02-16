import os
import shutil
import json
import logging


def setup_logging():
    logging.basicConfig(
        filename="file_organizer.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_config():
    with open("config.json", "r") as file:
        return json.load(file)


def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created folder: {path}")


def move_file(file_path, destination_folder):
    try:
        shutil.move(file_path, destination_folder)
        logging.info(f"Moved file: {file_path} -> {destination_folder}")
    except Exception as e:
        logging.error(f"Error moving file {file_path}: {str(e)}")


def organize_files():
    config = load_config()
    target_directory = config["target_directory"]
    categories = config["categories"]

    logging.info("Starting file organization process")

    for file_name in os.listdir(target_directory):
        file_path = os.path.join(target_directory, file_name)

        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_name)[1].lower()
            moved = False

            for category, extensions in categories.items():
                if file_extension in extensions:
                    destination_folder = os.path.join(target_directory, category)
                    create_folder_if_not_exists(destination_folder)
                    move_file(file_path, destination_folder)
                    moved = True
                    break

            # If no category matched, move to Others
            if not moved:
                others_folder = os.path.join(target_directory, "Others")
                create_folder_if_not_exists(others_folder)
                move_file(file_path, others_folder)

    logging.info("File organization process completed")


if __name__ == "__main__":
    setup_logging()
    organize_files()
