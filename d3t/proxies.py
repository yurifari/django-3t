class RenderedTemplate(object):
    def __init__(self, obj, context, nodes, result):
        self.obj = obj
        self.context = context
        self.nodes = nodes
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
