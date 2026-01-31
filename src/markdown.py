from htmlnode import ParentNode
from textnode import text_node_to_html_node
import inline
from blocks import block_to_block_type, BlockType, markdown_to_blocks
#md->blocks->inline->textnode->html
def text2kids(text):
    text_nodes = text
    kids = []
    for node in text_nodes:
        node = text_node_to_html_node(node)
        kids.append(node)
    return kids
def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    children = list()
    for block in block_list:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                paragraph = " ".join(lines)
                kids = text2kids(paragraph)
                children.append(ParentNode("p", kids))

    return ParentNode("div", children, None)
