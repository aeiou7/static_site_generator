from typing import final

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"tag = {self.tag}, val = {self.value}, children = {self.children}, props = {self.props_to_html()}"

    def to_html(self):
        raise NotImplementedError("to html isnt implemented yet")
    def props_to_html(self):
        retstr = ""
        if self.props:
            for key, value in self.props.items():
                retstr += f' {key}="{value}"'
        return retstr

class LeafNode(HTMLNode):
    @final
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if not self.value:
            raise ValueError("value was none")
        if not self.tag:
            return self.value
        propstr = ""
        if self.props:
            propstr = self.props_to_html()
        return f"<{self.tag}{propstr}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if not self.tag:
            raise ValueError("tag was none")
        if not self.children:
            raise ValueError("no children")
        propstr = ""
        if self.props:
            propstr = self.props_to_html()
        retstr = f"<{self.tag}{propstr}>"
        for i in self.children:
            retstr += i.to_html()
        retstr += f"</{self.tag}>"
        return retstr
