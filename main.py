import os
from datetime import datetime
from typing import Optional

import pillow_heif
from PIL import Image
from PIL.ExifTags import TAGS


def get_creation_date(image_path):
    try:
        if image_path.lower().endswith(".heic"):
            heif_file = pillow_heif.read_heif(image_path)
            exif_data = heif_file.to_pillow().getexif()
        else:
            image = Image.open(image_path)
            exif_data = image.getexif()

        if exif_data is not None:
            if image_path.lower().endswith(".heic"):
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == "DateTime":
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").date()
            else:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == "DateTimeOriginal":
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S").date()
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
    return None


def organize(directory: str) -> None:
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return

    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpeg", ".jpg", ".png", "heic")):
            file_path = os.path.join(directory, filename)
            creation_date = get_creation_date(file_path)
            if creation_date:
                date_folder = creation_date.strftime("%Y-%m-%d")
                date_folder_path = os.path.join(directory, date_folder)
                if not os.path.exists(date_folder_path):
                    os.makedirs(date_folder_path)
                os.rename(file_path, os.path.join(date_folder_path, filename))
                print(f"Moved {filename} to {date_folder}/")


if __name__ == "__main__":
    current_directory = os.getcwd()
    organize(current_directory)
    current_directory = os.getcwd()
    organize(current_directory)
