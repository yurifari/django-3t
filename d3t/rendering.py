from django.template.loader import get_template
from django.template.loader_tags import ExtendsNode

from d3t.watcher import watch

__all__ = [
    'render',
]


def defuse_extends_node(template):
    try:
        extends_node = template.nodelist.get_nodes_by_type(ExtendsNode)[0]
    except IndexError:
        pass
    else:
        extends_node.render = lambda *args, **kwargs: None
        template.nodelist += extends_node.nodelist


def render(template_name, context, using=None):
    template = get_template(template_name, using=using)

    defuse_extends_node(template.template)

    with watch() as rendered:
        template.render(context)

    return rendered
