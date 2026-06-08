import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(
                f"Invalid markdown syntax: unmatched delimiter '{delimiter}'"
            )

        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text) -> list[tuple]:
    return re.findall(
        r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",
        text
    )


def extract_markdown_links(text) -> list[tuple]:
    return re.findall(
        r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",
        text
    )


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if not images:
            new_nodes.append(node)
            continue

        last_index = 0

        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            start_index = node.text.find(image_markdown, last_index)

            if start_index > last_index:
                new_nodes.append(
                    TextNode(
                        node.text[last_index:start_index],
                        TextType.PLAIN_TEXT
                    )
                )

            new_nodes.append(
                TextNode(
                    alt_text,
                    TextType.IMAGE,
                    url
                )
            )

            last_index = start_index + len(image_markdown)

        if last_index < len(node.text):
            new_nodes.append(
                TextNode(
                    node.text[last_index:],
                    TextType.PLAIN_TEXT
                )
            )

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue

        last_index = 0

        for link_text, url in links:
            link_markdown = f"[{link_text}]({url})"
            start_index = node.text.find(link_markdown, last_index)

            if start_index > last_index:
                new_nodes.append(
                    TextNode(
                        node.text[last_index:start_index],
                        TextType.PLAIN_TEXT
                    )
                )

            new_nodes.append(
                TextNode(
                    link_text,
                    TextType.LINK,
                    url
                )
            )

            last_index = start_index + len(link_markdown)

        if last_index < len(node.text):
            new_nodes.append(
                TextNode(
                    node.text[last_index:],
                    TextType.PLAIN_TEXT
                )
            )

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]

    nodes = split_nodes_delimiter(
        nodes,
        "**",
        TextType.BOLD_TEXT
    )

    nodes = split_nodes_delimiter(
        nodes,
        "_",
        TextType.ITALIC_TEXT
    )

    nodes = split_nodes_delimiter(
        nodes,
        "`",
        TextType.CODE_TEXT
    )

    nodes = split_nodes_image(nodes)

    nodes = split_nodes_link(nodes)

    return nodes