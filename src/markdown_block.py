from enum import Enum

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")

    return [
        block.strip()
        for block in blocks
        if block.strip() != ""
    ]


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # Heading
    if block.startswith("#"):
        hash_count = 0

        for char in block:
            if char == "#":
                hash_count += 1
            else:
                break

        if 1 <= hash_count <= 6 and len(block) > hash_count and block[hash_count] == " ":
            return BlockType.HEADING

    # Code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote block
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list
    ordered = True

    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            ordered = False
            break

    if ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        # PARAGRAPH
        if block_type == BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            children.append(
                ParentNode(
                    "p",
                    text_to_children(text)
                )
            )

        # HEADING
        elif block_type == BlockType.HEADING:
            level = 0
            while level < len(block) and block[level] == "#":
                level += 1

            text = block[level:].strip()

            children.append(
                ParentNode(
                    f"h{level}",
                    text_to_children(text)
                )
            )

        # CODE
        elif block_type == BlockType.CODE:
            code_text = block[3:-3].strip("\n")

            code_node = LeafNode("code", code_text)

            children.append(
                ParentNode(
                    "pre",
                    [code_node]
                )
            )

        # QUOTE
        elif block_type == BlockType.QUOTE:
            lines = [
                line.lstrip(">").strip()
                for line in block.split("\n")
            ]

            quote_text = " ".join(lines)

            children.append(
                ParentNode(
                    "blockquote",
                    text_to_children(quote_text.strip())
                )
            )
        # UNORDERED LIST
        elif block_type == BlockType.UNORDERED_LIST:
            items = []

            for line in block.split("\n"):
                items.append(
                    ParentNode(
                        "li",
                        text_to_children(line[2:])
                    )
                )

            children.append(ParentNode("ul", items))

        # ORDERED LIST
        elif block_type == BlockType.ORDERED_LIST:
            items = []

            for line in block.split("\n"):
                text = line.split(". ", 1)[1]

                items.append(
                    ParentNode(
                        "li",
                        text_to_children(text)
                    )
                )

            children.append(ParentNode("ol", items))

        # PARAGRAPH fallback
        else:
            children.append(
                ParentNode(
                    "p",
                    text_to_children(block)
                )
            )

    return ParentNode("div", children)