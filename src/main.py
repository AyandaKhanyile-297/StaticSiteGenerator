from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from extrator import markdown_to_html_node

def main():
    markdown1 = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
This is text with a link [to boot dev](https://www.boot.dev) an image ![second image](https://i.imgur.com/3elNhQu.png)

"""

    markdown2 = """
This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)

> And this is a qoute

### Hastag Headings

- This is some list
- with some items
"""

    markdown3 = """
```
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
```

1. This is a list
2. with exactly 
3. 3 items
"""
    print((markdown_to_html_node(markdown1)).to_html())
    print("\n")
    print((markdown_to_html_node(markdown2)).to_html())
    print("\n")
    print((markdown_to_html_node(markdown3)).to_html())

main()