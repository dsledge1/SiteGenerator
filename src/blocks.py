import re
from enum import Enum
from htmlnode import *

def markdown_to_blocks(markdown):
    string = markdown.strip()
    blocks = re.split(r'\n\n+', string)
    for block in blocks:
        block = block.strip()

    return blocks

class BlockType(Enum):
    paragraph = 1
    heading = 2
    code = 3
    quote = 4
    unordered_list = 5
    ordered_list = 6

def block_to_block_type(block):
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return BlockType.heading
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.code
    elif block.startswith(">"):
        for line in block.splitlines():
            if not line.startswith(">"):
                break
            else:
                return BlockType.quote
        return BlockType.quote
    elif block.startswith("- "):
        for line in block.splitlines():
            if not line.startswith("-"):
                return BlockType.paragraph
            else:
                return BlockType.unordered_list
    elif re.match(r'^\d+\. ', block):
        for idx, line in enumerate(block.splitlines()):
            print(f"Line: {line}, Index: {idx+1}")
            print(f"First word: {line.split()[0]}")
            if not str(line.split()[0]) == f"{idx+1}.":
                return BlockType.paragraph
            else:
                continue
        return BlockType.ordered_list
    else:
        return BlockType.paragraph


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        obj = HTMLNode() #TODO Need a function for this
    return html_nodes

def text_to_children(text):
    pass
