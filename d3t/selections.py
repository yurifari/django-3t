class Selection(list):
    def __nonzero__(self):
        return self.__bool__()

    def __bool__(self):
        return len(self) > 0 and all(self)

    def __str__(self):
        return str([str(item) for item in self])

    def filter(self, condition):
        return self.__class__([item if condition(item) else None for item in self])

    def contains(self, content):
        return self.filter(lambda item: content in item.result)

    def equals(self, content):
        return self.filter(lambda item: content == item.result)


class TemplateSelection(Selection):
    def with_context(self, context):
        return self.filter(lambda item: all(i in item.context.items() for i in context.items()))


class NodeSelection(Selection):
    def within(self, template_name):
        return self.filter(lambda node: node.template.name == template_name)

    def with_arguments(self, *args, **kwargs):
        return self.filter(lambda node: node.arguments == (args, kwargs))
