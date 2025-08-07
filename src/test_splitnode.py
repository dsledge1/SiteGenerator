import unittest

from splitnode import *

class TestSplitNode(unittest.TestCase):

   
    def test_split(self):
        node = TextNode("This is a *text* node", TextType.NORMAL)
        result = split_nodes_delimiter([node], "*", TextType.NORMAL)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[1].text, "text")
        self.assertEqual(result[2].text, " node")

    def test_no_delimiter(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        result = split_nodes_delimiter([node], "*", TextType.NORMAL)
        self.assertEqual(node,result[0])

    def test_invalid_syntax(self):
        node = TextNode("This is a *text node", TextType.NORMAL)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "*", TextType.NORMAL)

    def test_different_text_type(self):
        node = TextNode("This is a *text* node", TextType.NORMAL)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)

        
        self.assertEqual(result[0].text, "This is a ")
        self.assertEqual(result[1].text, "text")
        self.assertEqual(result[2].text, " node")
        self.assertEqual(result[1].text_type, TextType.BOLD)

    def test_extract_markdown_images(self):
        text = "Here is an image: ![alt text](image_url)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0][0], "alt text")
        self.assertEqual(images[0][1], "image_url")

    def test_extract_markdown_links(self):
        text = "Here is a link: [link text](link_url)"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0][0], "link text")
        self.assertEqual(links[0][1], "link_url")

    def test_split_nodes_image(self):
        node = TextNode("Here is an image: ![alt text](image_url)", TextType.NORMAL)
        result = split_nodes_image([node])
        self.assertEqual(result[0].text, "Here is an image: ")
        self.assertEqual(result[1].text, "alt text")
        self.assertEqual(result[1].url, "image_url")

    def test_split_nodes_link(self):
        node = TextNode("Here is a link: [link text](link_url)", TextType.NORMAL)
        result = split_nodes_link([node])
        
        self.assertEqual(result[0].text, "Here is a link: ")
        self.assertEqual(result[1].url, "link_url")

    def test_split_nodes_link_multiple(self):
        node = TextNode("Here is a link: [link text](link_url) and another [another link](another_url)", TextType.NORMAL)
        result = split_nodes_link([node])
        self.assertEqual(result[0].text, "Here is a link: ")
        self.assertEqual(result[1].url, "link_url")
        self.assertEqual(result[2].text, " and another ")
        self.assertEqual(result[3].url, "another_url")

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is a text node without links", TextType.NORMAL)
        result = split_nodes_link([node])
        self.assertEqual(node, result[0])

    def test_split_images(self): #Example test i copied in
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )



    def test_split_nodes_links_and_images(self):
        node = TextNode(
            "This is *text* with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [linky](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = text_to_textnodes([node])
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.NORMAL),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a link ", TextType.NORMAL),
                TextNode("linky", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
