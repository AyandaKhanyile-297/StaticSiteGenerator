

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


