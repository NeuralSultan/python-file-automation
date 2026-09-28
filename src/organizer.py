from pathlib import Path
import shutil


FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "PDFs": [".pdf"],
    "Documents": [".doc", ".docx", ".txt", ".rtf"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
}


def get_category(file_path):
    """Return the category of a file based on its extension."""

    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_destination(destination):
    """Create a unique filename if the destination already exists."""

    if not destination.exists():
        return destination

    counter = 1

    while True:

        new_name = (
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )

        new_destination = (
            destination.parent / new_name
        )

        if not new_destination.exists():
            return new_destination

        counter += 1


def organize_files(source_folder, dry_run=False):
    """Organize files in the source folder by category."""

    source = Path(source_folder)

    if not source.exists():
        raise FileNotFoundError(
            f"Folder does not exist: {source}"
        )

    if not source.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {source}"
        )

    moved_files = []

    for file_path in source.iterdir():

        if not file_path.is_file():
            continue

        category = get_category(file_path)

        destination_folder = source / category

        destination_file = get_unique_destination(
            destination_folder / file_path.name
        )

        if dry_run:

            print(
                f"[DRY RUN] "
                f"{file_path.name} -> "
                f"{category}/{destination_file.name}"
            )

        else:

            destination_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.move(
                str(file_path),
                str(destination_file)
            )

            print(
                f"Moved: "
                f"{file_path.name} -> "
                f"{category}/{destination_file.name}"
            )

            moved_files.append(destination_file)

    return moved_files