from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

print("HI")

testdict = {"href": "https://google.com", "target": "_blank"}

def main():
    a=TextNode("abc","normal","lol.com")
    print(f"TextNode({a.text}, {a.text_type}, {a.url})")
    b=HTMLNode("abcd","jklol","A",testdict)
    print(b)
    print(HTMLNode.props_to_html(b))
    print(LeafNode("img", "", None, {"src":"","alt":""}).to_html())
    return
main()
