from django.template.loader_tags import ExtendsNode

from d3t.selections import NodeSelection, TemplateSelection

__all__ = [
    'RenderedTemplate',
    'RenderedNode',
    'RenderedResult',
]


class RenderedTemplate(object):
    def __init__(self, obj, context, nodes, parent_name, result):
        self.obj = obj
        self.context = context
        self.nodes = nodes
        self.parent_name = parent_name
        self.result = result

        for node in self.nodes:
            node.set_template(self)

    @property
    def name(self):
        return self.obj.name

    def __str__(self):
        return self.result

    def __eq__(self, other):
        return all([
            self.obj == other.obj,
            self.context == other.context,
            self.nodes == other.nodes,
            self.parent_name == other.parent_name,
        ])


class RenderedNode(object):
    def __init__(self, obj, result):
        self.obj = obj
        self.result = result
        self.template = None

    @property
    def name(self):
        try:
            return self.obj.token.split_contents()[0]
        except IndexError:
            return None

    @property
    def arguments(self):
        context = self.template.context
        get_resolved_arguments = self.obj.get_resolved_arguments

        try:
            args, kwargs = get_resolved_arguments(context)
        except AttributeError:
            args, kwargs = [], {}

        return tuple(args), kwargs

    def __str__(self):
        return self.result

    def __eq__(self, other):
        return all([
            self.obj == other.obj,
        ])

    def set_template(self, template):
        self.template = template


class RenderedResult(object):
    def __init__(self):
        self.nodes = []
        self.templates = []

    def _get_extended_template_name(self, nodelist, context):
        try:
            extends_node = nodelist.get_nodes_by_type(ExtendsNode)[0]
        except IndexError:
            return None

        return extends_node.parent_name.resolve(context)

    def register_template(self, sender, signal, template, context, result, **kwargs):
        parent_name = self._get_extended_template_name(template.nodelist, context)
        template = RenderedTemplate(template, context.dicts[-1], self.nodes[:], parent_name, result)
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
