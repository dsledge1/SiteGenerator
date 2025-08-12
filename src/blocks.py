import re
from enum import Enum
from htmlnode import *
from textnode import *
from splitnode import *

def markdown_to_blocks(markdown):
    string = markdown.strip()
    lines = string.splitlines()
    blocks = []
    current_block = []
    in_code_block = False
    current_block_type = None
    
    for line in lines:
        stripped_line = line.strip()
        
        # Handle code blocks specially
        if stripped_line.startswith("```"):
            if not in_code_block:
                # Start of code block
                if current_block:
                    blocks.append("\n".join(current_block))
                    current_block = []
                current_block.append(line)
                in_code_block = True
                current_block_type = "code"
            else:
                # End of code block
                current_block.append(line)
                blocks.append("\n".join(current_block))
                current_block = []
                in_code_block = False
                current_block_type = None
            continue
        
        # If we're in a code block, just add the line
        if in_code_block:
            current_block.append(line)
            continue
        
        # Empty line handling
        if stripped_line == "":
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
                current_block_type = None
            continue
        
        # Heading - always starts new block
        if re.match(r'^#{1,6} ', line):
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
            blocks.append(line)
            current_block_type = None
            continue
        
        # Determine line type
        line_type = None
        if line.startswith("> "):
            line_type = "quote"
        elif line.startswith("- ") or line.startswith("* "):
            line_type = "unordered_list"
        elif re.match(r'^\d+\. ', line):
            line_type = "ordered_list"
        else:
            line_type = "paragraph"
        
        # If block type changes, start new block
        if current_block_type and current_block_type != line_type:
            blocks.append("\n".join(current_block))
            current_block = []
        
        current_block.append(line)
        current_block_type = line_type
    
    # Add final block
    if current_block:
        blocks.append("\n".join(current_block))
    
    # Clean up blocks
    for idx, block in enumerate(blocks):
        blocks[idx] = block.strip()
    
    if not blocks:
        return [""]
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

            if not str(line.split()[0]) == f"{idx+1}.":
                return BlockType.paragraph
            else:
                continue
        return BlockType.ordered_list
    else:
        return BlockType.paragraph

def text_to_children(text):
    list = text_to_textnodes([TextNode(text, TextType.NORMAL)])
    new_list = []
    for node in list:
        new_list.append(text_to_html(node))
    return new_list
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

        
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block.strip() == "":
            continue
        elif block_type == BlockType.heading:
            new_block = block.splitlines()
            for line in new_block:
                if line.startswith("# "):
                    html_nodes.append(ParentNode("h1",text_to_children(line.strip("# "))))
                elif  line.startswith("## "):
                    html_nodes.append(ParentNode("h2",text_to_children(line.strip("## "))))
                elif line.startswith("### "):
                    html_nodes.append(ParentNode("h3",text_to_children(line.strip("### "))))
                elif line.startswith("#### "):
                    html_nodes.append(ParentNode("h4",text_to_children(line.strip("#### "))))
                elif line.startswith("##### "):
                    html_nodes.append(ParentNode("h5",text_to_children(line.strip("##### "))))
                elif line.startswith("###### "):
                    html_nodes.append(ParentNode("h6",text_to_children(line.strip("###### "))))
        elif block_type == BlockType.quote:
            lines = block.splitlines()
            quote_lines = [line.lstrip("> ").rstrip() for line in lines]
            quote_text = " ".join(quote_lines)
            html_nodes.append(ParentNode("blockquote",text_to_children(quote_text)))
        elif block_type == BlockType.paragraph:
            new_block = " ".join(block.splitlines())
            html_nodes.append(ParentNode("p",text_to_children(new_block)))
        elif block_type == BlockType.unordered_list:
            lines = block.splitlines()
            list_items = [line.lstrip("- ").rstrip() for line in lines]
            li_nodes = [ParentNode("li", text_to_children(item)) for item in list_items]
            ul_node = ParentNode("ul",li_nodes)
            html_nodes.append(ul_node)
        elif block_type == BlockType.ordered_list:
            lines = block.splitlines()
            list_items = [line.split(". ", 1)[1].rstrip() for line in lines if ". " in line]
            li_nodes = [ParentNode("li",text_to_children(item)) for item in list_items]
            ol_node = ParentNode("ol",li_nodes)
            html_nodes.append(ol_node)
        elif block_type == BlockType.code:
            code_content = block[4:-3] 
            node = TextNode(code_content, TextType.CODE)
            parent = ParentNode("pre",[text_to_html(node)])
            html_nodes.append(parent)   
    final_html = ParentNode("div", html_nodes)
    """print(f"Final HTML Node: {final_html}")
    print(f"Final HTML Node Children: {final_html.children}")"""
    return final_html


md = "- This is an unordered list item\n- This is another unordered list item\n- This is yet another unordered list item"
test = markdown_to_html_node(md)
#testleaf = LeafNode(test[0].tag, test[0].value)
print(test)
#print(testleaf)
#print(testleaf.to_html())