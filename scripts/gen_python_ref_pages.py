"""
Generate the code reference pages.

based on https://github.com/mkdocstrings/mkdocstrings/blob/33aa573efb17b13e7b9da77e29aeccb3fbddd8e8/docs/recipes.md
but modified for lack of "src/" file structure.

"""

from pathlib import Path
import shutil
import mkdocs_gen_files
import os
import shutil

# Clean a folder completely
def clean_folder(folder: Path):
    if folder.exists() and folder.is_dir():
        shutil.rmtree(folder)

root = Path(__file__).parent.parent
temp_dir = root / "temp_dir" / "python"

# Destination folders
destination_folders = [
    root / "docs" / "python",
    root / "docs" / "examples",
    root / "openml",
]

# Clean all destination folders
for folder in destination_folders:
    clean_folder(folder)

# Source folders
source_folders = [
    temp_dir / "docs",
    temp_dir / "examples",
    temp_dir / "openml",
]

# Copy source to destination
def copy_folders(source_folders: list[Path], destination_folders: list[Path]):
    if len(source_folders) != len(destination_folders):
        raise ValueError("Source and destination lists must have the same length.")

    for src, dest in zip(source_folders, destination_folders):
        if src.exists():
            shutil.copytree(src, dest)

copy_folders(source_folders, destination_folders)

# Generate the reference page docs
nav = mkdocs_gen_files.Nav()
root = Path(__file__).parent.parent
src = root / "openml"
edit_path_root = "/openml/openml-python/blob/docs/mkdoc/"

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(root).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    if len(parts) > 1 and not parts[1].startswith("_"):
        nav[parts[1:]] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        print("::: " + identifier, file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, Path(edit_path_root) / path.relative_to(root))

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())

# Generate the example page index
nav = mkdocs_gen_files.Nav()
examples_src = root / "docs" / "examples"
for path in sorted(examples_src.rglob("*.py")):
    dest_path = path.relative_to(examples_src)

    # Temporary. Renames the ugly folder names
    parts = list(dest_path.parts)
    parts[0] = parts[0].split("_", 1)[-1].capitalize()
    parts = tuple(parts) 

    if len(parts) > 1:
        nav[parts] = dest_path.as_posix()
with open(examples_src / "SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())

# Add icon to the reference pages
content_to_add = "---\nicon: material/bookshelf\n---\n\n"
index_file = root / "docs" / "python" / "index.md"
with open(index_file, "r+") as file:
    original_content = file.read()
    file.seek(0)
    file.write(content_to_add + original_content)
