from textnode import TextNode, TextType
from markdown import markdown_to_html_node
from htmlnode import HTMLNode
from os import listdir, path, mkdir
from pathlib import Path
from shutil import copy, rmtree
def copy_from_static_to_public(folder_path = "",file_list = listdir("static")):
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

def extract_title(markdown):
    if markdown:
        lines = markdown.split('\n')
        for line in lines:
            if not line.isspace() and line.lstrip()[0:2] == "# ":
                return line.lstrip()[2:].strip()
    raise ValueError
def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    from_content = Path(from_path).read_text()
    template_content = Path(template_path).read_text()
    html_node = markdown_to_html_node(from_content)
    html_node_content = html_node.to_html()
    title = extract_title(from_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_node_content)
    p = Path(dest_path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(template_content)
def generate_page_recursively(dir_path_content, template_path, dest_dir_path):
    content_list = listdir(dir_path_content)
    for content in content_list:
        content_path = f"{dir_path_content}/{content}"
        dir_path = f"{dest_dir_path}/{content}"
        if path.isdir(content_path):
            generate_page_recursively(content_path,template_path,dir_path)
        else:
            generate_page(content_path, template_path,f"{dir_path.rstrip(".md")}.html")



def main():
    copy_from_static_to_public()
    generate_page_recursively("content", "template.html", "public")

if __name__ == "__main__":
    main()
