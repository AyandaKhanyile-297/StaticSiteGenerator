from enum import Enum
         
class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "q"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"
    
class TextType(Enum):
    TEXT = ""
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"
        
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
            