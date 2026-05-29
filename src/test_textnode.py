import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("Different text", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Click me", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click me", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("Click me", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Click me", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("Plain text", TextType.PLAIN_TEXT, None)
        node2 = TextNode("Plain text", TextType.PLAIN_TEXT, None)
        self.assertEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold_text(self):
        node = TextNode("This is bold text", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

if __name__ == "__main__":
    unittest.main()