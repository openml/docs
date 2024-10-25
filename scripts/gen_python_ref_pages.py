"""Generate the code reference pages.

based on https://github.com/mkdocstrings/mkdocstrings/blob/33aa573efb17b13e7b9da77e29aeccb3fbddd8e8/docs/recipes.md
but modified for lack of "src/" file structure.

"""

from pathlib import Path
import shutil
import mkdocs_gen_files
import os
import shutil

# Move the python code and example folders into the root folder. This is necessary because the literate-nav has very strong
# opinions on where the files should be located. It refuses to work from the temp_dir directory.
def copy_folders_to_destinations(source_folders, destination_folders):
    """
    Copies folders from source to specified destinations and overwrites if they already exist.

    Parameters:
    - source_folders (list of str): List of paths to the source folders.
    - destination_folders (list of str): List of full paths to the target directories, including the new folder names.
    """
    if len(source_folders) != len(destination_folders):
        return

    # Copy each folder to its specified destination
    for src, dest in zip(source_folders, destination_folders):
        # Ensure the parent directory of the destination path exists
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        
        # Remove the folder if it already exists
        if os.path.exists(dest):
            shutil.rmtree(dest)
        
        # Copy the folder
        shutil.copytree(src, dest)

temp_dir = Path(__file__).parent.parent / "temp_dir" / "python"
source_folders = [
    temp_dir / "docs",
    temp_dir / "openml",
    temp_dir / "examples",
]
destination_folders = [
    Path(__file__).parent.parent / "docs" / "python",
    Path(__file__).parent.parent / "openml",
    Path(__file__).parent.parent / "docs" / "examples" # Move them straight here to avoid duplication. mkdocs-jupyter will handle them.
]
copy_folders_to_destinations(source_folders, destination_folders)

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