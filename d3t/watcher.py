from contextlib import contextmanager

from django.template.base import Node, Template

from .rendering import Rendering
from .signals import node_rendered, template_rendered

__all__ = [
    'watch_templates',
]


def wrap_template_render(render_function):
    def wrapper(template, context):
        result = render_function(template, context)
        template_rendered.send(sender=None, template=template, context=context, result=result)
        return result
    return wrapper


def wrap_node_render(render_function):
    def wrapper(node, context):
        result = render_function(node, context)
        node_rendered.send(sender=None, node=node, result=result)
        return result
    return wrapper


@contextmanager
def mock_template_render():
    original_function = Template._render
    Template._render = wrap_template_render(Template._render)

    yield

    Template._render = original_function


@contextmanager
def mock_node_render():
    original_function = Node.render_annotated
    Node.render_annotated = wrap_node_render(Node.render_annotated)

    yield

    Node.render_annotated = original_function


@contextmanager
def watch_templates():
    rendering = Rendering()

    template_rendered.connect(rendering.register_template)
    node_rendered.connect(rendering.register_node)

    with mock_template_render(), mock_node_render():
        yield rendering

    template_rendered.disconnect(rendering.register_template)
    node_rendered.disconnect(rendering.register_node)
