from htmlnode import ParentNode, LeafNode
from textnode import TextType
from markdown_block import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
import unittest

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        markdown = """This is a paragraph.

        This is another paragraph.

        This is a third paragraph."""
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "This is a paragraph.")
        self.assertEqual(blocks[1], "This is another paragraph.")
        self.assertEqual(blocks[2], "This is a third paragraph.")

    def test_markdown_with_empty_lines(self):
        markdown = """This is a paragraph.

        This is another paragraph.

        This is a third paragraph."""
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "This is a paragraph.")
        self.assertEqual(blocks[1], "This is another paragraph.")
        self.assertEqual(blocks[2], "This is a third paragraph.")

class TestBlockToBlockType(unittest.TestCase):
    
    def test_quote_block(self):
        block = "> This is a quote.\n> It has multiple lines."

        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.QUOTE)


    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"

        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.UNORDERED_LIST)


    def test_ordered_list_block(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"

        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.ORDERED_LIST)

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraph(self):
        markdown = "This is a paragraph."

        node = markdown_to_html_node(markdown)

        self.assertEqual(node.to_html(), "<div><p>This is a paragraph.</p></div>")


    def test_heading(self):
        markdown = "# Heading"

        node = markdown_to_html_node(markdown)

        self.assertEqual(node.to_html(), "<div><h1>Heading</h1></div>")


    def test_quote(self):
        markdown = "> This is a quote.\n> Second line"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote. Second line</blockquote></div>"
        )


    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        )


    def test_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><ol><li>Item 1</li><li>Item 2</li></ol></div>"
        )


    def test_code_block(self):
        markdown = "```\nprint('hi')\n```"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><pre><code>print('hi')</code></pre></div>"
        )


    def test_inline_formatting(self):
        markdown = "This is **bold** text and _italic_ text"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bold</b> text and <i>italic</i> text</p></div>"
        )