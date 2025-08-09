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

def text_to_children(text):
    list = text_to_textnodes(text)
    new_list = []
    for node in list:
        new_list.append(text_to_html(node))
    return new_list
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type ==BlockType.heading and block.startswith("# "):
            html_nodes.append(ParentNode("h1",None,text_to_children(block.strip("# "))))
        elif block_type ==BlockType.heading and block.startswith("## "):
            html_nodes.append(ParentNode("h2",None,text_to_children(block.strip("## "))))
        elif block_type ==BlockType.heading and block.startswith("### "):
            html_nodes.append(ParentNode("h3",None,text_to_children(block.strip("### "))))
        elif block_type ==BlockType.heading and block.startswith("#### "):
            html_nodes.append(ParentNode("h4",None,text_to_children(block.strip("#### "))))
        elif block_type ==BlockType.heading and block.startswith("##### "):
            html_nodes.append(ParentNode("h5",None,text_to_children(block.strip("##### "))))
        elif block_type ==BlockType.heading and block.startswith("###### "):
            html_nodes.append(ParentNode("h6",None,text_to_children(block.strip("###### "))))
        elif block_type == BlockType.quote:
            lines = block.splitlines()
            quote_lines = [line.lstrip("> ").rstrip() for line in lines]
            quote_text = "\n".join(quote_lines)
            html_nodes.append(ParentNode("blockquote", None,text_to_children(quote_text)))
        elif block_type == BlockType.paragraph:
            html_nodes.append(ParentNode("p",None,text_to_children(block)))
        elif block_type == BlockType.unordered_list:
            lines = block.splitlines()
            list_items = [line.lstrip("- ").rstrip() for line in lines]
            li_nodes = [ParentNode("li", None, text_to_children(item)) for item in list_items]
            ul_node = ParentNode("ul", None, li_nodes)
            html_nodes.append(ul_node)
        elif block_type == BlockType.ordered_list:
            lines = block.splitlines()
            list_items = [line.split(". ", 1)[1].rstrip() for line in lines if ". " in line]
            li_nodes = [ParentNode("li", None, text_to_children(item)) for item in list_items]
            ol_node = ParentNode("ol", None, li_nodes)
            html_nodes.append(ol_node)
        elif block_type == BlockType.code:
            code_content = block.strip("```").strip()
            node = TextNode(code_content, TextType.CODE)
            parent = ParentNode("pre", None, [text_to_html(node)])
            html_nodes.append(parent)   
    final_html = ParentNode("div", None, html_nodes)
    return final_html


md = "- This is an unordered list item\n- This is another unordered list item\n- This is yet another unordered list item"
test = markdown_to_html_node(md)
#testleaf = LeafNode(test[0].tag, test[0].value)
print(test)
#print(testleaf)
#print(testleaf.to_html())