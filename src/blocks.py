from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(string):
    parts = string.split('\n\n')
    new_parts = []
    for part in parts:
        tmp = part.strip()
        if tmp:
            new_parts.append(tmp)
    return new_parts


def block_to_block_type(block):
    if block[0] == '#':
        heading = False
        heading_count = 0
        i = 0
        for c in block[0:7]:
            if heading_count == 7:
                break
            if c == '#':
                heading = True
                heading_count +=1
            else:
                if c != " ":
                    heading = False
                break
            i +=1
        if heading and heading_count < 7:
            return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE
    elif block.startswith("> "):
        parts = block.split("\n")
        is_quote = True
        for part in parts:
            if part[0:2] != ("> "):
                is_quote = False
        if is_quote:
            return BlockType.QUOTE
    elif block.startswith("- "):
        parts = block.split("\n")
        is_unordered_list = True
        for part in parts:
            if part[0:2] != ("- "):
                is_unordered_list = False
        if is_unordered_list:
            return BlockType.UNORDERED_LIST
    elif block[0:3] == "1. ":
        parts = block.split("\n")
        index = 1
        list_exited = False
        for part in parts:
            if part[0:3] != f"{index}. ":
                list_exited = True
            index += 1
        if not list_exited:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

