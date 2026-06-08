import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_bold(self):
        old_nodes = [TextNode("This is **bold** text", TextType.PLAIN_TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD_TEXT)

        self.assertEqual(len(new_nodes), 3)

        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)

        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD_TEXT)

        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.PLAIN_TEXT)

    def test_unmatched_delimiter(self):
        old_nodes = [TextNode("This is **bold text", TextType.PLAIN_TEXT)]

        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD_TEXT)

        self.assertIn(
            "Invalid markdown syntax",
            str(context.exception)
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images(self):
        text = "Here is an image: ![alt text](image_url)"
        images = extract_markdown_images(text)

        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt text", "image_url"))

    def test_no_images(self):
        text = "This text has no images."
        images = extract_markdown_images(text)

        self.assertEqual(len(images), 0)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_links(self):
        text = "Here is a link: [Google](https://www.google.com)"
        links = extract_markdown_links(text)

        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("Google", "https://www.google.com"))

    def test_no_links(self):
        text = "This text has no links."
        links = extract_markdown_links(text)

        self.assertEqual(len(links), 0)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        old_nodes = [
            TextNode(
                "Here is an image: ![alt text](image_url)",
                TextType.PLAIN_TEXT
            )
        ]

        new_nodes = split_nodes_image(old_nodes)

        self.assertEqual(len(new_nodes), 2)

        self.assertEqual(new_nodes[0].text, "Here is an image: ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)

        self.assertEqual(new_nodes[1].text, "alt text")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "image_url")

    def test_no_images(self):
        old_nodes = [
            TextNode("This text has no images.", TextType.PLAIN_TEXT)
        ]

        new_nodes = split_nodes_image(old_nodes)

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This text has no images.")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        old_nodes = [
            TextNode(
                "Here is a link: [Google](https://www.google.com)",
                TextType.PLAIN_TEXT
            )
        ]

        new_nodes = split_nodes_link(old_nodes)

        self.assertEqual(len(new_nodes), 2)

        self.assertEqual(new_nodes[0].text, "Here is a link: ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)

        self.assertEqual(new_nodes[1].text, "Google")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://www.google.com")

    def test_no_links(self):
        old_nodes = [
            TextNode("This text has no links.", TextType.PLAIN_TEXT)
        ]

        new_nodes = split_nodes_link(old_nodes)

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This text has no links.")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)


if __name__ == "__main__":
    unittest.main()

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a "
            "`code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode(
                "link",
                TextType.LINK,
                "https://boot.dev",
            ),
        ]

        self.assertEqual(nodes, expected)

    def test_plain_text(self):
        text = "Just plain text"

        nodes = text_to_textnodes(text)

        expected = [
            TextNode("Just plain text", TextType.PLAIN_TEXT)
        ]

        self.assertEqual(nodes, expected)

    def test_single_bold(self):
        text = "**bold**"

        nodes = text_to_textnodes(text)

        expected = [
            TextNode("bold", TextType.BOLD_TEXT)
        ]

        self.assertEqual(nodes, expected)

    def test_single_link(self):
        text = "[Boot.dev](https://boot.dev)"

        nodes = text_to_textnodes(text)

        expected = [
            TextNode(
                "Boot.dev",
                TextType.LINK,
                "https://boot.dev"
            )
        ]

        self.assertEqual(nodes, expected)