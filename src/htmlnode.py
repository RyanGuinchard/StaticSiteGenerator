

class HTMLNode:

    def __init__(self, tag = None, value= None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method must be implemented by subclasses")

    def props_to_html(self):
        if not self.props:
            return ""
        prop_str = ""
        for key, value in self.props.items():
            prop_str += f' {key}="{value}"'
        return prop_str

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
        