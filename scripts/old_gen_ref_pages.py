"""Generate the code reference pages.

based on https://github.com/mkdocstrings/mkdocstrings/blob/33aa573efb17b13e7b9da77e29aeccb3fbddd8e8/docs/recipes.md
but modified for lack of "src/" file structure.

"""
from pathlib import Path
import mkdocs_gen_files
import os
import yaml
import shutil

nav = mkdocs_gen_files.Nav()

root = Path(__file__).parent.parent / "temp_dir" / "python"
src = root / "openml"

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

    nav[parts] = Path("../") / Path("reference", doc_path.as_posix())

    os.makedirs(os.path.dirname(root / full_doc_path), exist_ok=True)

    with open(root / full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        print("::: " + identifier, file=fd)
    #print(fd.name)

    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))

with open(root / "reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())


extra_nav_lines = [
    "* [Code Reference](reference/)\n",
    "* [Examples](examples/)\n",
]
print("Hello!")
# Rebuild the top nav, since mkdocs-multirepo and literate-nav don't play along
# Open the mkdocs.yml file and load the content
#with open(root / "mkdocs.yml", "r") as file:
#    mkdocs_content = yaml.safe_load(file)

# Extract the nav sections
#nav_sections = mkdocs_content.get("nav", [])

# Convert the nav sections to the literate format
#extra_nav_lines = []
#for item in nav_sections:
#    if isinstance(item, dict):
#        # Extract the key (section title) and value (file path)
#        for title, path in item.items():
#            line = f"* [{title}]({path})\n"
#            extra_nav_lines.append(line)
#    elif isinstance(item, str):
#        # Handle entries that are just strings (without a title)
#        line = f"* [Home]({item})\n"
#        extra_nav_lines.append(line)
with open(root / "SUMMARY.md", "w") as nav_file:
    nav_file.writelines(extra_nav_lines)

# Copy each .md file to the current directory and clean up
#docs_dir = root / "docs"
#for md_file in docs_dir.rglob("*.md"):
#    shutil.copy(md_file, root)
#shutil.rmtree(docs_dir)
#os.remove(root / "mkdocs.yml")

nav = mkdocs_gen_files.Nav()
examples_dir = root / "examples"
examples_doc_dir = root / "docs" / "examples"
for path in sorted(examples_dir.rglob("*.py")):
    dest_path = Path("examples") / path.relative_to(examples_dir)
    with mkdocs_gen_files.open(dest_path, "w") as dest_file:
        print(path.read_text(), file=dest_file)

    new_relative_location = Path("../") / dest_path
    nav[new_relative_location.parts[2:]] = new_relative_location.as_posix()

    with mkdocs_gen_files.open(root / "examples/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())

