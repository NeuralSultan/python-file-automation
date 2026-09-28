import argparse

from organizer import organize_files


def main():
    parser = argparse.ArgumentParser(
        description="Organize files automatically by type."
    )

    parser.add_argument(
        "--source",
        required=True,
        help="Path to the folder you want to organize"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files"
    )

    args = parser.parse_args()

    print("Starting file organizer...")

    if args.dry_run:
        print("DRY RUN mode: no files will be moved.\n")

    try:
        moved_files = organize_files(
            args.source,
            dry_run=args.dry_run
        )

        if not args.dry_run:
            print(
                f"\nCompleted! "
                f"{len(moved_files)} files organized."
            )

    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()