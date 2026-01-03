import unittest

from htmlnode import ParentNode, LeafNode

class testParentNode(unittest.TestCase):
    # --- Validation / error scenarios ---
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",)

    def test_parent_to_html_raises_when_tag_is_none(self):
        node = ParentNode(None, [LeafNode("span", "X")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_raises_when_children_is_none(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_raises_when_children_is_empty_list(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_raises_when_child_to_html_raises(self):
        # LeafNode with value None should raise; parent should propagate that error.
        bad_child = LeafNode("p", None)
        node = ParentNode("div", [bad_child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_children_must_be_iterable_otherwise_typeerror(self):
        # Optional: if your constructor allows non-list, the loop will fail.
        node = ParentNode("div", 123)  # not iterable
        with self.assertRaises(TypeError):
            node.to_html()

    # --- Basic rendering scenarios ---

    def test_parent_renders_single_leaf_child(self):
        node = ParentNode("div", [LeafNode("p", "Hello")])
        self.assertEqual(node.to_html(), "<div><p>Hello</p></div>")

    def test_parent_renders_multiple_leaf_children_in_order(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "One"),
                LeafNode("p", "Two"),
                LeafNode("span", "Three"),
            ],
        )
        self.assertEqual(node.to_html(), "<div><p>One</p><p>Two</p><span>Three</span></div>")

    def test_parent_renders_raw_text_leaf_child_when_tag_none(self):
        # LeafNode with tag None returns raw text
        node = ParentNode("div", [LeafNode(None, "raw")])
        self.assertEqual(node.to_html(), "<div>raw</div>")

    # --- Props scenarios ---

    def test_parent_includes_props_in_opening_tag(self):
        # This test assumes ParentNode.to_html() renders props in the opening tag:
        # f"<{self.tag}{self.props_to_html()}>"
        node = ParentNode("div", [LeafNode("span", "X")], {"class": "container", "id": "root"})
        html = node.to_html()

        # Order depends on dict insertion order; Python preserves insertion order.
        # We can assert exact string if we control insertion order:
        self.assertEqual(html, '<div class="container" id="root"><span>X</span></div>')

    def test_parent_props_empty_dict_same_as_no_props(self):
        node1 = ParentNode("div", [LeafNode("span", "X")], {})
        node2 = ParentNode("div", [LeafNode("span", "X")], None)
        self.assertEqual(node1.to_html(), node2.to_html())

    # --- Nesting scenarios ---

    def test_parent_renders_nested_parent_nodes(self):
        inner = ParentNode("div", [LeafNode("span", "Inner")])
        outer = ParentNode("section", [LeafNode("p", "Top"), inner, LeafNode("p", "Bottom")])
        self.assertEqual(
            outer.to_html(),
            "<section><p>Top</p><div><span>Inner</span></div><p>Bottom</p></section>",
        )

    def test_parent_deeply_nested_structure(self):
        level3 = ParentNode("em", [LeafNode(None, "deep")])
        level2 = ParentNode("span", [LeafNode(None, "A"), level3, LeafNode(None, "B")])
        level1 = ParentNode("p", [LeafNode(None, "Start "), level2, LeafNode(None, " End")])

        self.assertEqual(level1.to_html(), "<p>Start <span>A<em>deep</em>B</span> End</p>")

    # --- Mixed child types / robustness ---

    def test_parent_with_child_that_is_not_htmlnode_raises_attributeerror(self):
        # If a non-node is included, calling .to_html should fail.
        node = ParentNode("div", [LeafNode("p", "OK"), "not-a-node"])
        with self.assertRaises(AttributeError):
            node.to_html()

    def test_parent_with_tuple_children_iterable_ok(self):
        # If you allow any iterable, tuple should work.
        node = ParentNode("div", (LeafNode("p", "A"), LeafNode("p", "B")))
        self.assertEqual(node.to_html(), "<div><p>A</p><p>B</p></div>")



if __name__ == "__main__":
    unittest.main()
