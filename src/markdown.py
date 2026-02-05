from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline import text_to_textnodes
from blocks import block_to_block_type, BlockType, markdown_to_blocks
#md->blocks->inline->textnode->html
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    paragraph_node = []
    for block in block_list:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                paragraph = " ".join([line.strip() for line in block.splitlines(True)])
                text_nodes = text_to_textnodes(paragraph)
                kids = [text_node_to_html_node(tn) for tn in text_nodes]
                paragraph_node.append(ParentNode("p",kids))
            case BlockType.HEADING:
                paragraph = " ".join([line.strip() for line in block.splitlines(True)])
                stripped_par = paragraph.lstrip('#')
                stripped_par = stripped_par.lstrip(' ')
                text_nodes = text_to_textnodes(stripped_par)
                kids = [text_node_to_html_node(tn) for tn in text_nodes]
                headings = min(len(paragraph) - len(paragraph.lstrip('#')), 6)
                paragraph_node.append(ParentNode(f"h{headings}",kids))
            case BlockType.QUOTE:
                paragraph = "\n".join([line.lstrip("> ").rstrip("\n") for line in block.splitlines(True)])
                text_nodes = text_to_textnodes(paragraph)
                kids = [text_node_to_html_node(tn) for tn in text_nodes]
                paragraph_node.append(ParentNode("blockquote",[ParentNode("p",kids)]))
            case BlockType.CODE:
                paragraph = "\n".join([line.strip() for line in block.splitlines(True)])
                kids = [text_node_to_html_node(TextNode(paragraph.lstrip("""```""").rstrip("""```""").lstrip("\n").lstrip(" "),TextType.CODE))]# ai couldnt write code this bad
                paragraph_node.append(ParentNode("pre",kids))
            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                html_items = []
                for item in items:
                    text = item[2:]
                    children = text_to_children(text)
                    html_items.append(ParentNode("li", children))
                paragraph_node.append(ParentNode("ul", html_items))
            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                html_items = []
                for item in items:
                    parts = item.split(". ", 1)
                    text = parts[1]
                    children = text_to_children(text)
                    html_items.append(ParentNode("li", children))
                paragraph_node.append(ParentNode("ol", html_items))
    return ParentNode("div", paragraph_node, None)
