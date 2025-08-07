from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode():
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self,node2):
        if self.text == node2.text and self.text_type == node2.text_type and self.url == node2.url:
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_to_html(text_node):
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(None, text_node.text, None, None)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text, None, None)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text, None, None)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text, None, None)    
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, None, {"href":""})    
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", None, {"src":"","alt":""})
    else:
        raise Exception
