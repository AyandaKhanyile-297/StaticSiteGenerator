from enum import Enum
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINKS:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGES:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise ValueError("Invalid type!")
            
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            nodes_list = (node.text).split(delimiter)
            if len(nodes_list)%2 == 0:
                raise Exception("No closing delimiter")
            else:
                for i in range(len(nodes_list)):
                    if i%2 == 0:
                            new_nodes.append(TextNode(nodes_list[i], TextType.TEXT))
                    else:
                        if delimiter=="**":
                            new_nodes.append(TextNode(nodes_list[i], TextType.BOLD))
                        elif delimiter=="_":
                            new_nodes.append(TextNode(nodes_list[i], TextType.ITALIC))
                        elif delimiter=="`":
                            new_nodes.append(TextNode(nodes_list[i], TextType.CODE)) 
    return new_nodes
            
class TextType(Enum):
    TEXT = ""
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINKS = "a"
    IMAGES = "img"
    
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        if self.text == other.text:
            if self.text_type == other.text_type:
                if self.url == other.url:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
            
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
            