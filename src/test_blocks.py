import unittest

from blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    # 1) Split on double newline into blocks
    def test_splits_on_double_newline(self):
        md = "A\n\nB\n\nC"
        self.assertEqual(markdown_to_blocks(md), ["A", "B", "C"])

    # 2) Strips leading/trailing whitespace from the *entire document* effectively
    #    (achieved by stripping each block, plus discarding empties)
    def test_strips_leading_and_trailing_whitespace_document(self):
        md = "\n\n  A  \n\n  B\t\n\n"
        self.assertEqual(markdown_to_blocks(md), ["A", "B"])

    # 2) Strips leading/trailing whitespace from EACH block
    def test_strips_whitespace_each_block(self):
        md = "   A paragraph   \n\n\t\tAnother paragraph\t\t"
        self.assertEqual(markdown_to_blocks(md), ["A paragraph", "Another paragraph"])

    # 3) Removes empty blocks from excessive newlines
    def test_removes_empty_blocks_from_excessive_newlines(self):
        md = "A\n\n\n\nB\n\n\n\n\nC"
        # Splitting produces empty strings; those must be removed
        self.assertEqual(markdown_to_blocks(md), ["A", "B", "C"])

    # 3) Removes blocks that are whitespace-only (after strip they become empty)
    def test_removes_whitespace_only_blocks(self):
        md = "A\n\n   \n\n\t\n\nB"
        self.assertEqual(markdown_to_blocks(md), ["A", "B"])

    # 4) Preserves single newlines within a block (multi-line paragraph)
    def test_preserves_single_newlines_inside_paragraph_block(self):
        md = "Line 1\nLine 2\nLine 3\n\nNext block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Line 1\nLine 2\nLine 3", "Next block"],
        )

    # 4) Preserves list items within a list block (single newlines between items)
    def test_preserves_list_block_newlines(self):
        md = "- item 1\n- item 2\n- item 3\n\nAfter list"
        self.assertEqual(
            markdown_to_blocks(md),
            ["- item 1\n- item 2\n- item 3", "After list"],
        )

    # Edge explicitly implied by the starter test:
    # leading newline from triple-quoted string should not appear in first block
    def test_leading_newline_from_triple_quotes_not_included(self):
        md = """
First block

Second block
"""
        self.assertEqual(markdown_to_blocks(md), ["First block", "Second block"])

    # Edge explicitly implied by the starter test:
    # trailing newline at end should not appear in last block
    def test_trailing_newline_not_included_in_last_block(self):
        md = "A\n\nB\n"
        self.assertEqual(markdown_to_blocks(md), ["A", "B"])

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_levels_1_through_6(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_requires_space_after_hashes(self):
        # Must be 1-6 #'s followed by a space
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("##Heading"), BlockType.PARAGRAPH)

    def test_heading_more_than_6_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)

    def test_code_block_multiline_valid(self):
        md = "```\nprint('hi')\nprint('bye')\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_code_block_must_start_with_backticks_and_newline(self):
        # Must start with ```\n
        self.assertEqual(block_to_block_type("```print('hi')\n```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```\r\nprint('hi')\n```"), BlockType.PARAGRAPH)

    def test_code_block_must_end_with_backticks(self):
        self.assertEqual(block_to_block_type("```\nprint('hi')\n``"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```\nprint('hi')\n"), BlockType.PARAGRAPH)

    def test_quote_block_single_line_valid(self):
        self.assertEqual(block_to_block_type("> quoted text"), BlockType.QUOTE)

    def test_quote_block_multiline_valid(self):
        md = "> line one\n> line two\n> line three"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_unordered_list_block_single_line_valid(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_block_multiline_valid(self):
        md = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_unordered_list_block_every_line_must_start_with_dash_space(self):
        md = "- item 1\nitem 2\n- item 3"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

        md2 = "- item 1\n- item 2\n-* item 3"
        self.assertEqual(block_to_block_type(md2), BlockType.PARAGRAPH)

        md3 = "-item 1"
        self.assertEqual(block_to_block_type(md3), BlockType.PARAGRAPH)

    def test_ordered_list_block_single_line_valid(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.ORDERED_LIST)

    def test_ordered_list_block_multiline_valid_incrementing(self):
        md = "1. item one\n2. item two\n3. item three"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_ordered_list_block_must_start_at_1(self):
        md = "2. item one\n3. item two"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_ordered_list_block_must_increment_by_1_each_line(self):
        md = "1. item one\n3. item two"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

        md2 = "1. item one\n2. item two\n4. item three"
        self.assertEqual(block_to_block_type(md2), BlockType.PARAGRAPH)

    def test_ordered_list_block_requires_dot_and_space(self):
        md = "1.item one\n2. item two"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

        md2 = "1) item one\n2) item two"
        self.assertEqual(block_to_block_type(md2), BlockType.PARAGRAPH)

        md3 = "1.  item one"  # still has ". " at least once, but this is ambiguous; enforce strict ". " then text
        # If your implementation allows multiple spaces, change this expected value accordingly.
        self.assertEqual(block_to_block_type(md3), BlockType.ORDERED_LIST)

    def test_paragraph_fallback_when_no_other_rule_matches(self):
        self.assertEqual(block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("A paragraph\nwith a newline"), BlockType.PARAGRAPH)

    def test_mixed_list_like_blocks_are_paragraph(self):
        md = "- item\n2. item"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

        md2 = "> quote\n- list"
        self.assertEqual(block_to_block_type(md2), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
