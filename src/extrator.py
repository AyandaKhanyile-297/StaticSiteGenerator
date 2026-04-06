
import re
from textnode import TextNode, TextType, BlockType
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
    
def markdown_to_blocks(markdown):
    rawblocks = markdown.split("\n\n")
    final_blocks = []
    for block in rawblocks:
        new_block = block.removeprefix("\n")
        new_block = new_block.strip()
        final_blocks.append(new_block)
    return final_blocks
    
def block_to_block_type(markdown):    
    raw_block = (markdown_to_blocks(markdown))[0]
    if _is_heading(raw_block):
        return BlockType.HEADING
    elif _is_code(raw_block):
        return BlockType.CODE
    elif _is_quote(raw_block):
        return BlockType.QUOTE
    elif _is_unordered_list(raw_block):
        return BlockType.UNORDERED_LIST
    elif _is_ordered_list(raw_block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
        
def _is_heading(block_text):
    heading_tag = "#"
    for i in range(6):
        if block_text.startswith(f"{heading_tag} "):
            return True
        heading_tag += "#"
    return False

def _is_code(block_text):
    code_tag = "```"
    if block_text.startswith(f"{code_tag}\n"):
        if block_text.endswith(code_tag):
            return True
    return False
    
def _is_quote(block_text):
    quote_tag = ">"
    all_quotes = False
    for quotes in block_text.split("\n"):
        if (quotes.startswith(f"{quote_tag}")) or (quotes.startswith(f"{quote_tag} ")):
            all_quotes = True
    return all_quotes
    
def _is_unordered_list(block_text):
    ul_tag = "- "
    u_list = True
    for ul_items in block_text.split("\n"):
        if not (ul_items.startswith(f"{ul_tag}")):
            u_list =  False
    return u_list
    
def _is_ordered_list(block_text):
    o_list = True
    raw_list = block_text.split("\n")
    for ol_items in range(len(raw_list)):
        ol_tag = f"{ol_items+1}."
        if not (raw_list[ol_items].startswith(ol_tag)):
            o_list =  False
    return o_list
    