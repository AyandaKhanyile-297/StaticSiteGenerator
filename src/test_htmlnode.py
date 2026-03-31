import unittest

from htmlnode import HTMLNode

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