
import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

DELIMETER = {"**":TextType.BOLD, "_":TextType.ITALIC, "`":TextType.CODE}

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
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
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

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches
        
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches
    
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            if node.text != "":
                new_nodes.append(node)
        else:
            matches = extract_markdown_images(node.text)
            if len(matches) == 0:
                new_nodes.append(node)
            else:
                new_text = node.text
                for image in matches:
                    sections = new_text.split(f"![{image[0]}]({image[1]})")
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    new_text = sections[1]
                if new_text !="":
                    new_nodes.append(TextNode(new_text, TextType.TEXT))
    return new_nodes
            
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            if node.text != "":
                new_nodes.append(node)
        else:
            matches = extract_markdown_links(node.text)
            if len(matches) == 0:
                new_nodes.append(node)
            else:
                new_text = node.text
                for link in matches:
                    sections = new_text.split(f"[{link[0]}]({link[1]})")
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    new_text = sections[1]
                if new_text !="":
                    new_nodes.append(TextNode(new_text, TextType.TEXT))
    return new_nodes
    
def text_to_textnodes(text):
    final_nodes = [TextNode(text, TextType.TEXT)]
    
    for key in DELIMETER:
        final_nodes = split_nodes_delimiter(final_nodes, key, DELIMETER[key])
    
    final_nodes = split_nodes_image(final_nodes)
    final_nodes = split_nodes_link(final_nodes)
 
    return final_nodes
    

    