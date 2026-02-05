from markdown import markdown_to_html_node
from os import listdir, path, mkdir
from pathlib import Path
import shutil
from shutil import copy, rmtree
import sys
def copy_from_static_to_public(folder_path,file_list):
    if folder_path == "":
        print("removing public and making it")
        rmtree("public")
        mkdir("public")
    for f in file_list:
        file_path = f"static{folder_path}/{f}"
        file_path_public =  f"public/{folder_path}/{f}"
        if path.isdir(file_path):
            mkdir(file_path_public)
            copy_from_static_to_public(f"{folder_path}/{f}", listdir(file_path))
        elif path.isfile(file_path):
            copy(file_path,file_path_public)

def copy_directory_recursive(src: Path, dst: Path) -> None:
    if not dst.exists():
        dst.mkdir()

    for f in src.iterdir():
        new_f = dst / f.name
        if f.is_dir():
            copy_directory_recursive(f, new_f)
        else:
            print(f"Copying {f} to {new_f}")
            shutil.copy(f, new_f)

def extract_title(markdown):
    if markdown:
        lines = markdown.split('\n')
        for line in lines:
            if not line.isspace() and line.lstrip()[0:2] == "# ":
                return line.lstrip()[2:].strip()
    raise ValueError
def generate_page(from_path, template_path, dest_path, base_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    from_content = Path(from_path).read_text()
    template_content = Path(template_path).read_text()
    html_node = markdown_to_html_node(from_content)
    html_node_content = html_node.to_html()
    title = extract_title(from_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_node_content)
    template_content = template_content.replace('href="/', f'href="{base_path}/')
    template_content = template_content.replace('src="/', f'src="{base_path}/')
    p = Path(dest_path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(template_content)
def generate_page_recursively(dir_path_content, template_path, dest_dir_path, base_path):
    content_list = listdir(dir_path_content)
    for content in content_list:
        content_path = f"{dir_path_content}/{content}"
        dir_path = f"{dest_dir_path}/{content}"
        if path.isdir(content_path):
            generate_page_recursively(content_path,template_path,dir_path, base_path)
        else:
            generate_page(content_path, template_path,f"{dir_path.rstrip(".md")}.html", base_path)



def main():
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print(basepath)
    project_root = Path(__file__).parent.parent

    dest_path = project_root / "docs"
    static_dir = project_root / "static"
    if dest_path.exists():
        shutil.rmtree(dest_path)

    copy_directory_recursive(static_dir, dest_path)
    # copy_from_static_to_public()
    from_path = project_root / "content"
    template_path = project_root / "template.html"

    generate_page_recursively(from_path, template_path, dest_path, basepath)

if __name__ == "__main__":
    main()
