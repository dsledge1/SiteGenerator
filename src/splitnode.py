import re
from textnode import *
from htmlnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_list.append(node)
        if node.text_type == TextType.NORMAL and delimiter not in node.text:
            new_list.append(node)
        if delimiter in node.text and node.text_type == TextType.NORMAL:
            parts = node.text.split(delimiter)
            if len(parts) %2 == 0:
                raise Exception(f"Invalid markdown syntax: missing closing delimiter '{delimiter}'")
            for idx, part in enumerate(parts):
                if part:
                    new_type = ""
                    if delimiter == "*":
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
                        new_list.append(TextNode(part, text_type))
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
    image_check = []

    pattern = r'(!\[[^\]]*\]\([^\)]*\))'
    for node in old_nodes:

        images = extract_markdown_images(node.text)
        if not images:
            new_list.append(node)
    for image in images:

        image_check.append(image[0])
        image_check.append(image[1])
    if node.text_type == TextType.NORMAL:
        segments = re.split(pattern, node.text)

        for segment in segments:

            if not segment:
                continue
            if not re.match(pattern, segment):
                new_list.append(TextNode(segment, TextType.NORMAL))
            if re.match(pattern, segment):
                for image_alt, image_url in images:
                    if segment == f"![{image_alt}]({image_url})":
                        new_list.append(TextNode(image_alt, TextType.IMAGE, image_url))
                        break

    return new_list


def split_nodes_link(old_nodes):
    new_list = []
    links = []
    link_check = []

    pattern = r'(\[[^\]]*\]\([^\)]*\))'
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_list.append(node)
    for link in links:
        link_check.append(link[0])
        link_check.append(link[1])
    if node.text_type == TextType.NORMAL:
       
        segments = re.split(pattern, node.text)
        for segment in segments:
            if not segment:
                continue
            if not re.match(pattern, segment):
                new_list.append(TextNode(segment, TextType.NORMAL)) 
            if re.match(pattern, segment):
                for link_text, link_url in links:
                    if segment == f"[{link_text}]({link_url})":
                        new_list.append(TextNode(link_text, TextType.LINK, link_url))
                        break

    return new_list

def text_to_textnodes(old_nodes):
    new_nodes = old_nodes
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.NORMAL)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.NORMAL)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.NORMAL)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

testnode = TextNode(
            "This is *text* with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [linky](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL
)

def tester(node_list):
    final_list = []
    l1=split_nodes_image(node_list)
    for node in l1:
        a = split_nodes_link([node])
        print(a)


text_to_textnodes([testnode])
