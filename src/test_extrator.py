import unittest

from textnode import TextNode, TextType, BlockType
from extrator import extract_markdown_images, extract_markdown_links, text_node_to_html_node
from extrator import split_nodes_image, split_nodes_link, split_nodes_delimiter, text_to_textnodes
from extrator import markdown_to_blocks, block_to_block_type

class TestExtrator(unittest.TestCase):
    def test_spliter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        act_nodes = [TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes[0], act_nodes[0])
        self.assertEqual(new_nodes[1], act_nodes[1])
    
    def test_spliter_one_tag(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(cm.exception), "No closing delimiter")
        
    def test_spliter_two_tag(self):
        node = TextNode("This is `code` and more `code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        act_nodes = [TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and more ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT)]
        self.assertEqual(len(new_nodes), len(act_nodes))
    #=====  =====   =====  =====   =====  =====   =====  =====   =====  =====   #
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        answers = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(matches, answers)
        
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        answers = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(matches, answers)
        
    def test_not_extract_markdown_images(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        answers = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertNotEqual(matches, answers)
        
    def test_not_extract_markdown_links(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        answers = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertNotEqual(matches, answers)
    #=====  =====   =====  =====   =====  =====   =====  =====   =====  =====   #    
    def test_split_images_1(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,)
            
    def test_split_images_2(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and no other",
        TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and no other", TextType.TEXT)
            ],
            new_nodes,)
            
    def test_split_links_1(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes,)
            
    def test_split_links_2(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and no other",
        TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and no other", TextType.TEXT)
            ],
            new_nodes,)
    #=====  =====   =====  =====   =====  =====   =====  =====   =====  =====   #    
    def test_text_to_textnodes1(self):
        result = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        answer = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertListEqual(answer, result)
        
    def test_text_to_textnodes2(self):
        result = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and a [link](https://boot.dev)")
        answer = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertListEqual(answer, result)
    #=====  =====   =====  =====   =====  =====   =====  =====   =====  =====   #    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    #=====  =====   =====  =====   =====  =====   =====  =====   =====  =====   #    
    def test_blockParagraph(self):
        md = """
This is a paragraph
"""
        self.assertEqual(BlockType.PARAGRAPH ,block_to_block_type(md))
        
    def test_blockHeadings1(self):
        md = """
# This is a heading
"""
        self.assertEqual(BlockType.HEADING ,block_to_block_type(md))
        
    def test_blockHeadings2(self):
        md = """
##### This is also heading
"""
        self.assertEqual(BlockType.HEADING ,block_to_block_type(md))
        
    def test_blockHeadings3(self):
        md = """
###### This is still a heading
"""
        self.assertEqual(BlockType.HEADING ,block_to_block_type(md))
        
    def test_blockHeadings4(self):
        md = """
####### This is not heading
"""
        self.assertNotEqual(BlockType.HEADING ,block_to_block_type(md))
        
    def test_blockCode(self):
        md = """
```

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

```
"""
        self.assertNotEqual(BlockType.CODE,block_to_block_type(md))
    
    def test_blockQuote1(self):
        md = """
>This is a quote
"""
        self.assertEqual(BlockType.QUOTE,block_to_block_type(md))
        
    def test_blockQuote2(self):
        md = """
> This is also a quote
>surely
"""
        self.assertEqual(BlockType.QUOTE,block_to_block_type(md))
    
    def test_blockUnorderedList(self):
        md = """
- This is a list
- with items
"""
        self.assertEqual(BlockType.UNORDERED_LIST,block_to_block_type(md))
      
    def test_blockOrderedList(self):
        md = """
1. This is a list
2. with exactly 
3. 3 items
"""
        self.assertEqual(BlockType.ORDERED_LIST,block_to_block_type(md))
      
    #=====  =====   =====  =====   =====  =====   =====  =====   =====  =====   #    
    