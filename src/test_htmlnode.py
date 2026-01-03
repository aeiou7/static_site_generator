import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init_sets_values(self):
        node = HTMLNode(
            tag="p",
            value="hello",
            children=["child1", "child2"],
            props={"class": "greeting"},
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.children, ["child1", "child2"])
        self.assertEqual(node.props, {"class": "greeting"})

    def test_init_defaults(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_init_values_not_equal_when_different(self):
        node1 = HTMLNode(tag="p", value="a", children=[], props={"class": "x"})
        node2 = HTMLNode(tag="div", value="a", children=[], props={"class": "x"})
        node3 = HTMLNode(tag="p", value="b", children=[], props={"class": "x"})
        node4 = HTMLNode(tag="p", value="a", children=["child"], props={"class": "x"})
        node5 = HTMLNode(tag="p", value="a", children=[], props={"id": "y"})

        self.assertNotEqual(node1.tag, node2.tag)
        self.assertNotEqual(node1.value, node3.value)
        self.assertNotEqual(node1.children, node4.children)
        self.assertNotEqual(node1.props, node5.props)

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="p", value="hello", children=[], props={})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_empty_props(self):
        node = HTMLNode(tag="p", value="hello", children=[], props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(tag="a", value="link", children=[], props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple_props_preserves_insertion_order(self):
        props = {"href": "https://example.com", "target": "_blank"}
        node = HTMLNode(tag="a", value="link", children=[], props=props)
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_props_to_html_none_props_behaves_reasonably(self):
        # If you decide that props=None should be treated as "no attributes",
        # this test locks that in.
        node = HTMLNode(tag="p", value="hello", children=[], props=None)
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
