import unittest

from htmlnode import LeafNode

class testLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_raw_text_when_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_raises_value_error_if_value_missing(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_img_like_still_renders_open_close(self):
        # (Even if "img" is normally self-closing, this assignment typically doesn't special-case it.)
        node = LeafNode("span", "X", {"class": "badge"})
        self.assertEqual(node.to_html(), '<span class="badge">X</span>')

if __name__ == "__main__":
    unittest.main()
