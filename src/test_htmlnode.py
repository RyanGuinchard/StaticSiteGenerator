import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("div", "Hello", None, {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "container"})

    def test_props_to_html_no_props(self):
        node = HTMLNode("div")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLNode("div", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')