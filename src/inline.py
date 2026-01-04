from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        string_parts = node.text.split(delimiter)
        if((len(string_parts)) % 2 == 0):
            raise Exception("no even ammount of delimiters")

        for i, part in enumerate(string_parts):
            if (node.text[0] == delimiter
                and i == 0 or
                node.text[len(node.text)-1] == delimiter
                and i == len(string_parts)-1):
                continue
            if i % 2 > 0:
                new_list.append(TextNode(part, text_type))
            else:
                new_list.append(TextNode(part, TextType.TEXT))

    return new_list

# URL allows balanced parentheses groups, but does not allow spaces.
# Handles parentheses (one level deep) inside the URL.
_MD_URL = r"[^()\s]+(?:\([^()\s]*\)[^()\s]*)*"

def extract_markdown_images(text):
    return re.findall(rf"!\[([^\[\]]*)\]\(({_MD_URL})\)", text)

def extract_markdown_links(text):
    return re.findall(rf"(?<!!)\[([^\[\]]*)\]\(({_MD_URL})\)", text)

_IMAGE_TOKEN_RE = re.compile(rf"!\[([^\[\]]*)\]\(({_MD_URL})\)")
_IMAGE_OPEN_RE  = re.compile(r"!\[")

def split_nodes_images_helper(text):
    pattern = rf"!\[[^\]]*\]\({_MD_URL}\)"
    return re.sub(pattern, ",", text)

def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        text = node.text

        # Validate: any image-like opener must belong to a valid token
        opens = list(_IMAGE_OPEN_RE.finditer(text))
        matches = list(_IMAGE_TOKEN_RE.finditer(text))
        if opens:
            covered = [False] * len(opens)
            for m in matches:
                s, e = m.span()
                for j, o in enumerate(opens):
                    if s <= o.start() < e:
                        covered[j] = True
            if not all(covered):
                raise Exception("Invalid markdown image")
        images = extract_markdown_images(text)
        string_parts = split_nodes_images_helper(text).split(',')
        for i, part in enumerate(string_parts):
            if part:
                new_list.append(TextNode(part, TextType.TEXT))
            if i < len(images):
                new_list.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))

    return new_list

_LINK_TOKEN_RE = re.compile(rf"(?<!!)\[([^\[\]]*)\]\(({_MD_URL})\)")
_LINK_OPEN_RE  = re.compile(r"(?<!!)\[")  # any link-like "[" not preceded by "!"

def split_nodes_links_helper(text):
    # links only, not images
    pattern = rf"(?<!!)\[[^\]]*\]\({_MD_URL}\)"
    return re.sub(pattern, ",", text)

def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        text = node.text

        # 1) Validate: any link-like opener must belong to a valid token
        opens = list(_LINK_OPEN_RE.finditer(text))
        matches = list(_LINK_TOKEN_RE.finditer(text))
        if opens:
            covered = [False] * len(opens)
            for m in matches:
                s, e = m.span()
                for j, o in enumerate(opens):
                    if s <= o.start() < e:
                        covered[j] = True
            if not all(covered):
                raise Exception("Invalid markdown link")

        links = extract_markdown_links(text)
        string_parts = split_nodes_links_helper(text).split(',')
        for i, part in enumerate(string_parts):
            if part:
                new_list.append(TextNode(part, TextType.TEXT))
            if i < len(links):
                new_list.append(TextNode(links[i][0], TextType.LINK, links[i][1]))

    return new_list

def text_to_textnodes(text):
    new_list = [TextNode(text,TextType.TEXT)]
    new_list = (split_nodes_delimiter(new_list, "**", TextType.BOLD))
    new_list = (split_nodes_delimiter(new_list, "_", TextType.ITALIC))
    new_list = (split_nodes_delimiter(new_list, "'", TextType.CODE))
    new_list = (split_nodes_image(new_list))
    new_list = (split_nodes_link(new_list))
    return new_list
