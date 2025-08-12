import re
from textnode import *
from htmlnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_list.append(node)
        elif node.text_type == TextType.NORMAL and delimiter not in node.text:
            new_list.append(node)
        elif delimiter in node.text and node.text_type == TextType.NORMAL:
            parts = node.text.split(delimiter)
            if len(parts) %2 == 0:
                raise Exception(f"Invalid markdown syntax: missing closing delimiter '{delimiter}'")
            for idx, part in enumerate(parts):
                if part:
                    new_type = ""
                    if delimiter == "**":
                        new_type = TextType.BOLD
                    elif delimiter == "_":
                        new_type = TextType.ITALIC
                    elif delimiter == "`":
                        new_type = TextType.CODE
                    elif delimiter == "[":
                        new_type = TextType.LINK
                    elif delimiter == "!":
                        new_type = TextType.IMAGE
                    else:
                        raise Exception(f"Unknown delimiter: {delimiter}")
                    if idx % 2 == 0:
                        new_list.append(TextNode(part, TextType.NORMAL))
                    else:
                        new_list.append(TextNode(part, new_type))

    return new_list

def extract_markdown_images(text):
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_pattern, text)
    return matches

def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_list = []
    images = []


    pattern = r'(!\[[^\]]*\]\([^\)]*\))'
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if node.text_type != TextType.NORMAL:
            new_list.append(node)
        elif node.text_type == TextType.NORMAL:
            segments = re.split(pattern, node.text)
            for segment in segments:
                if not segment:
                    continue
                elif not re.match(pattern, segment):
                    new_list.append(TextNode(segment, TextType.NORMAL))
                elif re.match(pattern, segment):
                    for image_alt, image_url in images:
                        if segment == f"![{image_alt}]({image_url})":
                            new_list.append(TextNode(image_alt, TextType.IMAGE, image_url))
                            break
                


    return new_list


def split_nodes_link(old_nodes):
    new_list = []
    links = []


    pattern = r'(\[[^\]]*\]\([^\)]*\))'
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if node.text_type != TextType.NORMAL:
            new_list.append(node)
        elif node.text_type == TextType.NORMAL:
            segments = re.split(pattern, node.text)
            for segment in segments:
                if not segment:
                    continue
                elif not re.match(pattern, segment):
                    new_list.append(TextNode(segment, TextType.NORMAL)) 
                elif re.match(pattern, segment):
                    for link_text, link_url in links:
                        if segment == f"[{link_text}]({link_url})":
                            new_list.append(TextNode(link_text, TextType.LINK, link_url))
                            break



    return new_list

def text_to_textnodes(old_nodes):
    if old_nodes == "":
        return []
    new_nodes = old_nodes
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes) 
    return new_nodes

testnode = TextNode(
            "This is **text** with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [linky](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL
)

testnode2 = TextNode(
            "- This is an unordered list item\n- This is another unordered list item\n- This is yet another unordered list item",
            TextType.NORMAL
)

def tester(node_list):
    final_list = []
    l1=split_nodes_image(node_list)
    for node in l1:
        a = split_nodes_link([node])
        print(a)


print(text_to_textnodes([testnode]))