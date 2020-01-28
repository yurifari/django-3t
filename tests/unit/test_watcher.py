from django.template import Context, Template

from d3t.signals import node_rendered, template_rendered
from d3t.watcher import watch


def test_signals_connection(mocker):
    register_template = mocker.patch('d3t.watcher.RenderedResult.register_template')
    register_node = mocker.patch('d3t.watcher.RenderedResult.register_node')

    with watch():
        template_rendered.send(None)
        node_rendered.send(None)

    assert register_template.called
    assert register_node.called


def test_signals_disconnection(mocker):
    register_template = mocker.patch('d3t.watcher.RenderedResult.register_template')
    register_node = mocker.patch('d3t.watcher.RenderedResult.register_node')

    with watch():
        pass

    template_rendered.send(None)
    node_rendered.send(None)

    assert not register_template.called
    assert not register_node.called


def test_signal_sending(mocker):
    on_template_rendered = mocker.Mock()
    on_node_rendered = mocker.Mock()

    template_rendered.connect(on_template_rendered)
    node_rendered.connect(on_node_rendered)

    template = Template(
        '{% load echo from tags %}'
        '{% echo %}'
    )

    with watch():
        template.render(Context())

    assert on_template_rendered.called
    assert on_node_rendered.called
