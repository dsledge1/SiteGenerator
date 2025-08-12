class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        worklist=[]
        for k,v in self.props.items():
             worklist.append((f'{k}="{v}"'))
        html = " " + " ".join(worklist)
        return html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


    def __eq__(self,node2):
        if self.tag == node2.tag and self.value == node2.value and self.children == node2.children and self.props == node2.props:
            return True
        else:
            return False

class LeafNode(HTMLNode):
    def __init__(self,tag=None,value=None, children=None, props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        else:
            if self.tag == "a":
                return f'<a{self.props_to_html()}>{self.value}</a>'
            elif self.tag == "img":
                return f'<img{self.props_to_html()} />'
            else:
                return f'<{self.tag}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag specified")
        if self.children == None:
            raise ValueError("Must have children")
        else:
            lst = []
            for child in self.children:
                lst.append(child.to_html())
            return f'<{self.tag}>{"".join(lst)}</{self.tag}>'  
