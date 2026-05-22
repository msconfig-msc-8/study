from __future__ import annotations

import argparse
import fnmatch
import os
import shutil
from pathlib import Path


DEFAULT_OUTPUT_SUFFIX = "_clean"

EXCLUDED_DIR_NAMES = {
    ".git",
    ".hg",
    ".idea",
    ".mypy_cache",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    ".vscode",
    "__pycache__",
    "_ai_export",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "venv",
}

EXCLUDED_FILE_NAMES = {
    ".coverage",
    ".DS_Store",
    "desktop.ini",
    "Thumbs.db",
}

EXCLUDED_FILE_PATTERNS = {
    "*.bak",
    "*.log",
    "*.pyd",
    "*.pyo",
    "*.pyc",
    "*.tmp",
    "*.swp",
    "*.swo",
    "data_broken_*.json",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy this project to a new folder without generated files."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Destination folder. Default: sibling folder named <project>_clean.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Delete the destination folder first if it already exists.",
    )
    return parser.parse_args()


def should_skip_dir(path: Path, source: Path, output: Path) -> bool:
    if path.resolve() == output:
        return True

    name = path.name
    if name in EXCLUDED_DIR_NAMES:
        return True

    try:
        relative = path.relative_to(source)
    except ValueError:
        return False

    return relative.parts and relative.parts[0].endswith(DEFAULT_OUTPUT_SUFFIX)


def should_skip_file(path: Path) -> bool:
    if path.name in EXCLUDED_FILE_NAMES:
        return True

    return any(fnmatch.fnmatch(path.name, pattern) for pattern in EXCLUDED_FILE_PATTERNS)


def copy_clean_project(source: Path, output: Path, overwrite: bool = False) -> tuple[int, int]:
    source = source.resolve()
    output = output.resolve()

    if output == source:
        raise ValueError("Output folder must be different from the source project folder.")

    if output.exists():
        if not overwrite:
            raise FileExistsError(
                f"Destination already exists: {output}\n"
                f"Use --overwrite or choose another folder with --output."
            )
        shutil.rmtree(output)

    copied_files = 0
    skipped_items = 0

    for root, dir_names, file_names in os.walk(source):
        root_path = Path(root)

        kept_dir_names = []
        for dir_name in dir_names:
            dir_path = root_path / dir_name
            if should_skip_dir(dir_path, source, output):
                skipped_items += 1
                continue
            kept_dir_names.append(dir_name)
        dir_names[:] = kept_dir_names

        for file_name in file_names:
            item = root_path / file_name
            if item == output or output in item.parents:
                skipped_items += 1
                continue

            if should_skip_file(item):
                skipped_items += 1
                continue

            relative_path = item.relative_to(source)
            target = output / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            copied_files += 1

    return copied_files, skipped_items


def main() -> None:
    args = parse_args()
    source = Path(__file__).resolve().parent
    output = args.output or source.with_name(f"{source.name}{DEFAULT_OUTPUT_SUFFIX}")

    copied_files, skipped_items = copy_clean_project(source, output, args.overwrite)

    print(f"Clean project folder: {output}")
    print(f"Copied files: {copied_files}")
    print(f"Skipped items: {skipped_items}")


if __name__ == "__main__":
    main()
