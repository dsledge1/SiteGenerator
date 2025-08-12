import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p","abcd","A","B")
        node2 = HTMLNode("p","abcd","A","B")
        self.assertEqual(node,node2)

    def test_ineq(self):
        node = HTMLNode("p","abcd","A","B")
        node2 = HTMLNode("x","abcd","A","B")
        self.assertNotEqual(node,node2)

    def test_None(self):
        node = HTMLNode("p","abcd","A")
        node2 = HTMLNode("p","abcd","A")
        self.assertEqual(node,node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p","Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Link!",None, {"href": "https://www.lol.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.lol.com">Link!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child", None)
        parent_node = ParentNode("div", [child_node], None)
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild", None)
        child_node = ParentNode("span", [grandchild_node], None)
        parent_node = ParentNode("div", [child_node], None)
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


