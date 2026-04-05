import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from extrator import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        links = {
        "href": "https://www.google.com",
        "target": "_blank",
        }
        node = HTMLNode("<p>","This is a text", None, links)
        test_string = " href=https://www.google.com target=_blank"
        self.assertEqual(node.props_to_html(), test_string)
        
    def test_uneq_props_to_html(self):
        node = HTMLNode("<p>","This is a text")
        test_string = " href=https://www.google.com target=_blank"
        self.assertNotEqual(node.props_to_html(), test_string)
    
    def test_eq_props_to_html(self):
        links = {
        "target": "_blank",
        }
        node = HTMLNode("<p>","This is still text", None, links)
        test_string = " target=_blank"
        self.assertEqual(node.props_to_html(), test_string)
    #=====  =====   =====  =====   =====  =====   =====  =====   =====  =====   #    
    def test_leaf_to_html(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "\"https://example.com\""})
        self.assertEqual(node.to_html(), "<a href=\"https://example.com\">Click me!</a>")    
    #=====  =====   =====  =====   =====  =====   =====  =====   =====  =====   #    
    def test_parent_to_html(self):
        node = ParentNode(
        "p",
        [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )
    
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div")
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_with_no_tag(self):
        parent_node = ParentNode()
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        self.assertEqual(str(cm.exception), "Missing tag!")
        
    def test_to_html_with_nested_children(self):
        child1_node = LeafNode("span", "child 1")
        parent1_node = ParentNode("div", [child1_node])
        child2_node = LeafNode("span", "child 2")
        parent2_node = ParentNode("p", [child2_node, parent1_node])
        self.assertEqual(parent2_node.to_html(), "<p><span>child 2</span><div><span>child 1</span></div></p>")
    #=====  =====   =====  =====   =====  =====   =====  =====   =====  =====   #    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    
    def test_text(self):
        node = TextNode("This is a link node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
    #=====  =====   =====  =====   =====  =====   =====  =====   =====  =====   #    
        
    