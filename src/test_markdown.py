import unittest
from markdown import markdown_to_html_node

class testMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading(self):
        md = """
# This is a **heading** with _inline_ `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <b>heading</b> with <i>inline</i> <code>code</code></h1></div>",
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "</code></pre></div>",
        )

    def test_quote(self):
        md = """
> This is a **quote**
> with _two_ lines and `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>quote</b>\n"
            "with <i>two</i> lines and <code>code</code></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item with **bold**
- Item with _italic_ and `code`
- Plain item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul>"
            "<li>Item with <b>bold</b></li>"
            "<li>Item with <i>italic</i> and <code>code</code></li>"
            "<li>Plain item</li>"
            "</ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First **item**
2. Second _item_
3. Third with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol>"
            "<li>First <b>item</b></li>"
            "<li>Second <i>item</i></li>"
            "<li>Third with <code>code</code></li>"
            "</ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
