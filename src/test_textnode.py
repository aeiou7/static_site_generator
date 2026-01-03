import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a link node", TextType.LINK, "www.test.com")
        node2 = TextNode("This is a link node", TextType.LINK, "www.test.com")
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_url_none_on_no_input(self):
        node = TextNode("This is a link node", TextType.LINK)
        node2 =TextNode("this is a image node", TextType.IMAGE)
        self.assertEqual(node.url, None)
        self.assertEqual(node2.url, None)
    def test_url(self):
        node = TextNode("This is a link node", TextType.LINK, "www.text.com")
        node2 =TextNode("this is a image node", TextType.IMAGE, "www.text.com")
        self.assertNotEqual(node.url, None)
        self.assertEqual(node.url, "www.text.com")
        self.assertNotEqual(node2.url, None)
        self.assertEqual(node2.url, "www.text.com")
    def test_url_none_on_not_link(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        self.assertEqual(node.url, None)

class Test_text_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(len(html_node.props), 2)
        self.assertEqual(html_node.props["alt"], node.text)
    def test_two_uneq(self):
        node1 = TextNode("This is a text node", TextType.LINK)
        html_node1 = text_node_to_html_node(node1)
        node2 = TextNode("This is a text node", TextType.CODE)
        html_node2 = text_node_to_html_node(node2)
        self.assertNotEqual(html_node1.tag, html_node2.tag)
        self.assertNotEqual(html_node1.props, html_node2.props)

if __name__ == "__main__":
    unittest.main()
