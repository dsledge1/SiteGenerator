import re
from enum import Enum
from htmlnode import *
from textnode import *
from splitnode import *

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
        if block_type ==BlockType.heading and block.startswith("# "):
            html_nodes.append(HTMLNode("h1",block.strip("# ")))
        elif block_type ==BlockType.heading and block.startswith("## "):
            html_nodes.append(HTMLNode("h2",block.strip("## ")))
        elif block_type ==BlockType.heading and block.startswith("### "):
            html_nodes.append(HTMLNode("h3",block.strip("### ")))
        elif block_type ==BlockType.heading and block.startswith("#### "):
            html_nodes.append(HTMLNode("h4",block.strip("#### ")))
        elif block_type ==BlockType.heading and block.startswith("##### "):
            html_nodes.append(HTMLNode("h5",block.strip("##### ")))
        elif block_type ==BlockType.heading and block.startswith("###### "):
            html_nodes.append(HTMLNode("h6",block.strip("###### ")))
        elif block_type == BlockType.quote:
            lines = block.splitlines()
            quote_lines = [line.lstrip("> ").rstrip() for line in lines]
            quote_text = "\n".join(quote_lines)
            html_nodes.append(HTMLNode("blockquote", quote_text))
        elif block_type == BlockType.paragraph:
            html_nodes.append(HTMLNode("p", block))
        elif block_type == BlockType.unordered_list:
            lines = block.splitlines()
            list_items = [line.lstrip("- ").rstrip() for line in lines]
            li_nodes = [HTMLNode("li", item) for item in list_items]
            ul_node = ParentNode("ul", None, li_nodes)
            html_nodes.append(ul_node)
    return html_nodes

def text_to_children(text):
    pass

md = "- This is an unordered list item\n- This is another unordered list item\n- This is yet another unordered list item"
test = markdown_to_html_node(md)
#testleaf = LeafNode(test[0].tag, test[0].value)
print(test)
#print(testleaf)
#print(testleaf.to_html())