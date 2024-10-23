"""Generate the code reference pages.

based on https://github.com/mkdocstrings/mkdocstrings/blob/33aa573efb17b13e7b9da77e29aeccb3fbddd8e8/docs/recipes.md
but modified for lack of "src/" file structure.

"""

from pathlib import Path
import shutil
import mkdocs_gen_files
import os
import shutil

# Move the python folders into the docs. This is necessary because the literate-nav has very strong
# opinions on where the files should be located. It refused to work from the temp_dir directory.

def copy_folders_to_destinations(source_folders, destination_folders):
    """
    Copies folders from source to specified destinations and overwrites if they already exist.

    Parameters:
    - source_folders (list of str): List of paths to the source folders.
    - destination_folders (list of str): List of full paths to the target directories, including the new folder names.
    """
    if len(source_folders) != len(destination_folders):
        print("Error: The number of source folders must match the number of destination folders.")
        return

    # Copy each folder to its specified destination
    for src, dest in zip(source_folders, destination_folders):
        # Ensure the parent directory of the destination path exists
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        
        # Remove the folder if it already exists
        if os.path.exists(dest):
            shutil.rmtree(dest)
            print(f"Removed existing folder: {dest}")
        
        # Copy the folder
        shutil.copytree(src, dest)
        print(f"Copied {src} to {dest}")

# Example usage
temp_dir = Path(__file__).parent.parent / "temp_dir" / "python"
source_folders = [
    temp_dir / "openml",
    temp_dir / "examples",
    temp_dir / "docs"
]
destination_folders = [
    Path(__file__).parent.parent / "openml",
    Path(__file__).parent.parent / "examples",
    Path(__file__).parent.parent / "docs" / "python"
]
copy_folders_to_destinations(source_folders, destination_folders)


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
    print(full_doc_path)
    print(path.relative_to(root))

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())

nav = mkdocs_gen_files.Nav()
examples_dir = root / "examples"
for path in sorted(examples_dir.rglob("*.py")):
    dest_path = Path("example_refs") / path.relative_to(examples_dir)
    with mkdocs_gen_files.open(dest_path, "w") as dest_file:
        print(path.read_text(), file=dest_file)
        print(dest_path.name)

    new_relative_location = Path("../") / dest_path
    nav[new_relative_location.parts[2:]] = new_relative_location.as_posix()

with mkdocs_gen_files.open("example_refs/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
