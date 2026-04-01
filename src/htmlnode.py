

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self):
        result = ""
        if self.props != None:
            for prop in self.props:
                result += f" {prop}={self.props[prop]}"
        return result
        
    def __repr__(self):
        return f"Tag:{self.tag} Value:{self.value} Children={self.children} Props={self.props_to_html()}"

    def to_html(self):
        raise NotImplementedError("Override")

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Missing tag!")
        if self.children == None:
            raise ValueError("Missing children!")
        else:
            leaves = f"<{self.tag}>"
            for leaf in self.children:
                leaves += leaf.to_html()
            return leaves+f"</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("Missing value!")
        if self.tag == None:
            return self.value
        else:
            if self.props == None:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"Tag:{self.tag} Value:{self.value} Props={self.props_to_html()}"



