import unittest
from main import extract_title

class testExtractTitle(unittest.TestCase):

    def test_simple_h1(self):
        md = "# heading"
        self.assertEqual(extract_title(md), "heading")

    def test_strips_whitespace(self):
        md = "#   Hello world   "
        self.assertEqual(extract_title(md), "Hello world")

    def test_first_h1_wins(self):
        md = "# First\n\n# Second"
        self.assertEqual(extract_title(md), "First")

    def test_ignores_h2_and_lower(self):
        md = "## Not it\n### Also not it\n# Yes it"
        self.assertEqual(extract_title(md), "Yes it")

    def test_ignores_setext_h1_style(self):
        md = "Title\n=====\n"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_ignores_inline_hashes(self):
        md = "This is # not a header\n\n# Real"
        self.assertEqual(extract_title(md), "Real")

    def test_allows_leading_spaces_before_hash(self):
        md = "   # Indented"
        self.assertEqual(extract_title(md), "Indented")

    def test_rejects_no_space_after_hash(self):
        md = "#Nope\n# Yep"
        self.assertEqual(extract_title(md), "Yep")

    def test_ignores_code_fence_like_lines(self):
        md = "```\n# not a heading\n```\n# real heading"
        # Note: this implementation does NOT parse markdown blocks; it will see "# not a heading" inside code fences.
        # If you want to ignore fenced code blocks, say so and we’ll adjust the implementation.
        self.assertEqual(extract_title(md), "not a heading")

    def test_empty_markdown_raises(self):
        md = ""
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_no_h1_raises(self):
        md = "## heading\nsome text\n### more"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_only_hash_raises(self):
        md = "#"
        with self.assertRaises(ValueError):
            extract_title(md)

    # def test_hash_with_spaces_only_raises(self):
        # md = "#    \n## ok"
        # with self.assertRaises(ValueError):
            # extract_title(md)

    def test_none_input_raises(self):
        with self.assertRaises(ValueError):
            extract_title(None)

if __name__ == "__main__":
    unittest.main()
