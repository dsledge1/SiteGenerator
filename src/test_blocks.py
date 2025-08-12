import unittest

from blocks import *

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,[
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])

    def test_markdown_to_blocks_single_line(self):
        md = "This is a single line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line"])

    def test_markdown_to_blocks_multiple_newlines(self):
        md = "Line 1\n\nLine 2\n\n\nLine 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line 1", "Line 2", "Line 3"])

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        md = "   This is a line with leading and trailing spaces   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a line with leading and trailing spaces"])
    
    def test_markdown_to_blocks_mixed_content(self):
        md = "This is a **bolded** paragraph\n\nThis is another paragraph with _italic_ text and `code` here"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is a **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here"
        ])

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.paragraph)

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.heading)

    def test_block_to_block_type_code(self): 
        block = "```\nThis is code\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.code)
    def test_block_to_block_type_quote(self):
        block = "> This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.quote)   
    def test_block_to_block_type_unordered_list(self):
        block = "- This is an unordered list item\n- This is another unordered list item\n- This is yet another unordered list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.unordered_list)
    def test_block_to_block_type_ordered_list(self):
        block = "1. This is an ordered list item\n2. This is another ordered list item\n3. This is yet another ordered list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ordered_list)
    def test_block_to_block_type_not_ordered_list(self):
        block = "1. This is an ordered list item\n3. This is another unordered list item\n10. This is yet another unordered list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.paragraph)
    def test_block_to_block_type_empty(self):
        block = ""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.paragraph)
     
    def test_markdown_to_html_node(self):
        md = "# Heading 1\n\nThis is a paragraph with **bold** text and _italic_ text.\n\n- List item 1\n- List item 2\n\n> This is a quote.\n\n```\nCode block\n```"
        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 5)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_block_quote(self):
        md = """
> This is a quote
> with multiple lines
> and some **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and some <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_heading(self):
        md = """
# Heading 1
## Heading 2
### Heading 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_mixed_content(self):
        md = """
# Heading
This is a paragraph with **bold** text and _italic_ text.
- List item 1
- List item 2
> This is a quote.
```
Code block
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>Heading</h1>", html)
        self.assertIn("<p>This is a paragraph with <b>bold</b> text and <i>italic</i> text.</p>", html)
        self.assertIn("<ul><li>List item 1</li><li>List item 2</li></ul>", html)
        self.assertIn("<blockquote>This is a quote.</blockquote>", html)
        self.assertIn("<pre><code>Code block\n</code></pre>", html)        