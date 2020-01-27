from django.dispatch import Signal

__all__ = [
    'node_rendered',
    'template_rendered',
]


template_rendered = Signal(providing_args=['template', 'context', 'result'])
node_rendered = Signal(providing_args=['node', 'result'])
