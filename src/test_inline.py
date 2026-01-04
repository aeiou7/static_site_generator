import unittest

from textnode import TextNode, TextType
from inline import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes  # adjust if needed


class TestSplitNodesDelimiter(unittest.TestCase):
    def testDelimitCode(self):
        node1 = TextNode("hello `code` world", TextType.TEXT)
        test1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(
            test1,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" world", TextType.TEXT),
            ],
        )

    def testDelimitBold(self):
        node1 = TextNode("hello **bold** world", TextType.TEXT)
        test1 = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(
            test1,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" world", TextType.TEXT),
            ],
        )

    def testDelimitItalic(self):
        node1 = TextNode("hello _italic_ world", TextType.TEXT)
        test1 = split_nodes_delimiter([node1], "_", TextType.ITALIC)
        self.assertEqual(
            test1,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" world", TextType.TEXT),
            ],
        )

    def testNoDelimiterNoChange(self):
        node1 = TextNode("hello world", TextType.TEXT)
        test1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(test1, [TextNode("hello world", TextType.TEXT)])


    def testNonTextNodeUnchanged(self):
        node1 = TextNode("already bold", TextType.BOLD)
        test1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(test1, [TextNode("already bold", TextType.BOLD)])


    def testMultipleDelimitersSameNodeCode(self):
        node1 = TextNode("a `b` c `d` e", TextType.TEXT)
        test1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(
            test1,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("b", TextType.CODE),
                TextNode(" c ", TextType.TEXT),
                TextNode("d", TextType.CODE),
                TextNode(" e", TextType.TEXT),
            ],
        )


    def testDelimiterAtStart(self):
        node1 = TextNode("`code` world", TextType.TEXT)
        test1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(
            test1,
            [
                TextNode("code", TextType.CODE),
                TextNode(" world", TextType.TEXT),
            ],
        )


    def testDelimiterAtEnd(self):
        node1 = TextNode("hello `code`", TextType.TEXT)
        test1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(
            test1,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )


    def testPreservesOtherNodesInList(self):
        node1 = TextNode("hello `code` world", TextType.TEXT)
        node2 = TextNode("BOLD", TextType.BOLD)
        node3 = TextNode("x `y` z", TextType.TEXT)
        test1 = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        self.assertEqual(
            test1,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" world", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
                TextNode("x ", TextType.TEXT),
                TextNode("y", TextType.CODE),
                TextNode(" z", TextType.TEXT),
            ],
        )


    def testUnmatchedDelimiterRaises(self):
        node1 = TextNode("hello `code world", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node1], "`", TextType.CODE)


    def testUnmatchedDelimiterRaisesBold(self):
        node1 = TextNode("hello **bold world", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node1], "**", TextType.BOLD)


    def testUnmatchedDelimiterRaisesItalic(self):
        node1 = TextNode("hello _italic world", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node1], "_", TextType.ITALIC)


    def testAdjacentDelimitersEmptySegment(self):
        """
        If your implementation allows empty formatted segments, this should pass.
        If you chose to reject them, change this test to assertRaises instead.
        """
        node1 = TextNode("a `` b", TextType.TEXT)
        test1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(
            test1,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("", TextType.CODE),
                TextNode(" b", TextType.TEXT),
            ],
        )

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a [link](https://boot.dev)"
        )
        self.assertListEqual([("link", "https://boot.dev")], matches)
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_images_multiple(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )


    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("No images here, just text.")
        self.assertListEqual([], matches)


    def test_extract_markdown_images_ignores_links(self):
        text = "A link [boot dev](https://www.boot.dev) but no images."
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)


    def test_extract_markdown_images_alt_text_with_spaces(self):
        matches = extract_markdown_images(
            "Look ![two words](https://example.com/two.png) ok"
        )
        self.assertListEqual([("two words", "https://example.com/two.png")], matches)


    def test_extract_markdown_images_url_with_querystring(self):
        matches = extract_markdown_images(
            "Image ![pic](https://example.com/img.png?size=large&x=1)"
        )
        self.assertListEqual(
            [("pic", "https://example.com/img.png?size=large&x=1")],
            matches,
        )


    def test_extract_markdown_images_parens_in_url(self):
        # Many simple regexes won't support parentheses in URLs; if yours does, keep this.
        # If your implementation doesn't, remove this test or adjust to your intended behavior.
        matches = extract_markdown_images(
            "Image ![x](https://example.com/a(b)c.png)"
        )
        self.assertListEqual(
            [("x", "https://example.com/a(b)c.png")],
            matches,
        )


    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)


    def test_extract_markdown_links_multiple(self):
        text = (
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )


    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("No links here.")
        self.assertListEqual([], matches)


    def test_extract_markdown_links_ignores_images(self):
        text = "An image ![alt](https://example.com/a.png) but no links."
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)


    def test_extract_markdown_links_anchor_text_with_spaces(self):
        matches = extract_markdown_links(
            "See [two words](https://example.com/path) ok"
        )
        self.assertListEqual([("two words", "https://example.com/path")], matches)


    def test_extract_markdown_links_url_with_querystring(self):
        matches = extract_markdown_links(
            "Link [x](https://example.com/page?ref=abc&x=1)"
        )
        self.assertListEqual(
            [("x", "https://example.com/page?ref=abc&x=1")],
            matches,
        )


    def test_extract_markdown_links_does_not_match_image_syntax(self):
        # Ensures link extractor does not accidentally match inside ![...](...)
        text = "Image ![alt text](https://example.com/a.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)


    def test_extract_markdown_images_and_links_together(self):
        text = (
            "Text ![img](https://example.com/a.png) "
            "and [link](https://example.com)"
        )
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("img", "https://example.com/a.png")], img_matches)
        self.assertListEqual([("link", "https://example.com")], link_matches)


class TestSplitNodesImages(unittest.TestCase):
    def test_split_images_given_example(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_single_middle(self):
        node = TextNode(
            "Hello ![alt](https://example.com/a.png) world",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://example.com/a.png"),
                TextNode(" world", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_at_start(self):
        node = TextNode(
            "![alt](https://example.com/a.png) after",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "https://example.com/a.png"),
                TextNode(" after", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_at_end(self):
        node = TextNode(
            "before ![alt](https://example.com/a.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://example.com/a.png"),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_adjacent_images(self):
        node = TextNode(
            "a ![one](https://ex.com/1.png)![two](https://ex.com/2.png) b",
            TextType.TEXT,
        )
        # Expect: no empty TextNodes inserted between adjacent images
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "https://ex.com/1.png"),
                TextNode("two", TextType.IMAGE, "https://ex.com/2.png"),
                TextNode(" b", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_no_images_returns_original(self):
        nodes = [TextNode("plain text only", TextType.TEXT)]
        self.assertListEqual(nodes, split_nodes_image(nodes))

    def test_split_images_non_text_nodes_passthrough(self):
        nodes = [
            TextNode("prefix ", TextType.TEXT),
            TextNode("already a link", TextType.LINK, "https://x.com"),
            TextNode("![img](https://ex.com/a.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("prefix ", TextType.TEXT),
                TextNode("already a link", TextType.LINK, "https://x.com"),
                TextNode("img", TextType.IMAGE, "https://ex.com/a.png"),
            ],
            new_nodes,
        )

    def test_split_images_ignores_links(self):
        node = TextNode(
            "before [label](https://example.com) after",
            TextType.TEXT,
        )
        # split_nodes_image should not touch link markdown
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_images_url_with_parentheses(self):
        node = TextNode(
            "x ![alt](https://en.wikipedia.org/wiki/Foo_(bar)) y",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("x ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://en.wikipedia.org/wiki/Foo_(bar)"),
                TextNode(" y", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_unicode_alt_and_url(self):
        node = TextNode(
            "a ![café](https://example.com/über.png) b",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("café", TextType.IMAGE, "https://example.com/über.png"),
                TextNode(" b", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_images_invalid_markdown_raises(self):
        # Missing closing ')'
        node = TextNode(
            "bad ![alt](https://example.com/a.png",
            TextType.TEXT,
        )
        with self.assertRaises(Exception):
            split_nodes_image([node])


class TestSplitNodesLinks(unittest.TestCase):
    def test_split_links_given_example(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_single_middle(self):
        node = TextNode(
            "Hello [site](https://example.com) world",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://example.com"),
                TextNode(" world", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_at_start(self):
        node = TextNode(
            "[site](https://example.com) after",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("site", TextType.LINK, "https://example.com"),
                TextNode(" after", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_at_end(self):
        node = TextNode(
            "before [site](https://example.com)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://example.com"),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_adjacent_links(self):
        node = TextNode(
            "a [one](https://ex.com/1)[two](https://ex.com/2) b",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://ex.com/1"),
                TextNode("two", TextType.LINK, "https://ex.com/2"),
                TextNode(" b", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_no_links_returns_original(self):
        nodes = [TextNode("plain text only", TextType.TEXT)]
        self.assertListEqual(nodes, split_nodes_link(nodes))

    def test_split_links_non_text_nodes_passthrough(self):
        nodes = [
            TextNode("prefix ", TextType.TEXT),
            TextNode("already image", TextType.IMAGE, "https://x.com/a.png"),
            TextNode("[x](https://ex.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("prefix ", TextType.TEXT),
                TextNode("already image", TextType.IMAGE, "https://x.com/a.png"),
                TextNode("x", TextType.LINK, "https://ex.com"),
            ],
            new_nodes,
        )

    def test_split_links_ignores_images(self):
        node = TextNode(
            "before ![alt](https://example.com/a.png) after",
            TextType.TEXT,
        )
        # split_nodes_link should not touch image markdown
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links_url_with_parentheses(self):
        node = TextNode(
            "x [alt](https://en.wikipedia.org/wiki/Foo_(bar)) y",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("x ", TextType.TEXT),
                TextNode("alt", TextType.LINK, "https://en.wikipedia.org/wiki/Foo_(bar)"),
                TextNode(" y", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_unicode_label_and_url(self):
        node = TextNode(
            "a [café](https://example.com/über) b",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("a ", TextType.TEXT),
                TextNode("café", TextType.LINK, "https://example.com/über"),
                TextNode(" b", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_links_invalid_markdown_raises(self):
        # Missing closing ')'
        node = TextNode(
            "bad [alt](https://example.com",
            TextType.TEXT,
        )
        with self.assertRaises(Exception):
            split_nodes_link([node])

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_assignment_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_text_to_textnodes_plain_text_only(self):
        text = "Just some plain text."
        self.assertListEqual(
            [TextNode("Just some plain text.", TextType.TEXT)],
            text_to_textnodes(text),
        )

    def test_text_to_textnodes_only_formatting(self):
        text = "**bold** _italic_ `code`"
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            text_to_textnodes(text),
        )

    def test_text_to_textnodes_multiple_links_and_images(self):
        text = (
            "Start [a](https://a.com) mid "
            "![img](https://i.imgur.com/x.png) and "
            "[b](https://b.com) end"
        )
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode(" mid ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://i.imgur.com/x.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.LINK, "https://b.com"),
                TextNode(" end", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )

    def test_text_to_textnodes_parentheses_in_url(self):
        text = "See [wiki](https://en.wikipedia.org/wiki/Foo_(bar)) now"
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode("wiki", TextType.LINK, "https://en.wikipedia.org/wiki/Foo_(bar)"),
                TextNode(" now", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )

    def test_text_to_textnodes_adjacent_tokens_no_empty_textnodes(self):
        text = "![a](https://a.com/a.png)[b](https://b.com)**c**_d_`e`"
        # Expect no empty TEXT nodes; tokens should be in correct order.
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://a.com/a.png"),
                TextNode("b", TextType.LINK, "https://b.com"),
                TextNode("c", TextType.BOLD),
                TextNode("d", TextType.ITALIC),
                TextNode("e", TextType.CODE),
            ],
            text_to_textnodes(text),
        )

    def test_text_to_textnodes_invalid_link_markdown_raises(self):
        text = "bad [alt](https://example.com"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_text_to_textnodes_invalid_image_markdown_raises(self):
        text = "bad ![alt](https://example.com/image.png"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_text_to_textnodes_invalid_bold_markdown_raises(self):
        # Assuming your split_nodes_delimiter raises on unmatched delimiters
        text = "bad **bold"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_text_to_textnodes_invalid_italic_markdown_raises(self):
        text = "bad _italic"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_text_to_textnodes_invalid_code_markdown_raises(self):
        text = "bad `code"
        with self.assertRaises(Exception):
            text_to_textnodes(text)
if __name__ == "__main__":
    unittest.main()
