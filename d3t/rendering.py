from .proxies import RenderedNode, RenderedTemplate
from .selections import NodeSelection, TemplateSelection

__all__ = [
    'Rendering',
]


class Rendering(object):
    def __init__(self):
        self.nodes = []
        self.templates = []

    def register_template(self, sender, signal, template, context, result, **kwargs):
        template = RenderedTemplate(template, context.dicts[-1], self.nodes[:], result)
        self.templates.append(template)
        self.nodes = []

    def register_node(self, sender, signal, node, result, **kwargs):
        node = RenderedNode(node, result)
        self.nodes.append(node)

    def template(self, name):
        return TemplateSelection([
            template
            for template in self.templates
            if template.name == name
        ])

    def node(self, name):
        return NodeSelection([
            node
            for template in self.templates
            for node in template.nodes
            if node.name == name
        ])

    def block(self, name):
        return NodeSelection([
            node
            for node in self.node('block')
            if node.obj.name == name
        ])
