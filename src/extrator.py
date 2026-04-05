
import re
from textnode import TextNode, TextType

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
