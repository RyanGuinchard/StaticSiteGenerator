from gencontent import extract_title
import unittest

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
        # My Title

        This is some content.
        """

        title = extract_title(markdown)
        self.assertEqual(title, "My Title")

    def test_no_title(self):
        markdown = """
        This is some content without a title.
        """

        with self.assertRaises(Exception) as context:
            extract_title(markdown)

        self.assertTrue("No h1 header found" in str(context.exception))
