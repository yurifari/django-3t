import pytest
from django.template import Context

from d3t.proxies import RenderedNode, RenderedTemplate
from d3t.rendering import Rendering


@pytest.fixture
def make_template(mocker):
    def inner(name=None, context=None, result=None):
        template = mocker.Mock()
        template.name = name or ''
        template.context = context or {}
        template.result = result
        template.nodes = []
        return template
    return inner


@pytest.fixture
def make_node(mocker):
    def inner(template, name=None, args=None, kwargs=None, result=None):
        node = mocker.Mock()
        node.name = name or ''
        node.template = template
        node.arguments = (args or [], kwargs or {})
        node.result = result
        template.nodes.append(node)
        return node
    return inner


@pytest.fixture
def make_block(mocker, make_node):
    def inner(template, name=None):
        block = make_node(template, 'block')
        block.obj = mocker.Mock()
        block.obj.name = name
        return block
    return inner


@pytest.fixture
def make_rendering(mocker):
    def inner(templates=None):
        rendering = Rendering()
        rendering.templates = templates or []
        return rendering
    return inner


def test_template_registration(mocker):
    context = {'key': 'value'}
    request_context = Context({})
    request_context.update(context)
    template = mocker.Mock()
    nodes = [mocker.Mock()]
    result = mocker.Mock()
    rendering = Rendering()
    rendering.nodes = nodes

    rendering.register_template(mocker.ANY, mocker.ANY, template, request_context, result)

    assert rendering.templates == [RenderedTemplate(template, context, nodes, result)]


def test_node_registration(mocker):
    node = mocker.Mock()
    result = mocker.Mock()
    rendering = Rendering()

    rendering.register_node(mocker.ANY, mocker.ANY, node, result)

    assert rendering.nodes == [RenderedNode(node, result)]


def test_template(make_template, make_rendering):
    template1 = make_template('right')
    template2 = make_template('wrong')
    template3 = make_template('right')
    rendering = make_rendering([template1, template2, template3])

    assert rendering.template('right') == [template1, template3]


def test_node(make_template, make_node, make_rendering):
    template = make_template()
    node1 = make_node(template, 'right')
    _ = make_node(template, 'wrong')
    node3 = make_node(template, 'right')
    rendering = make_rendering([template])

    assert rendering.node('right') == [node1, node3]


def test_block(make_node, make_block, make_template, make_rendering):
    template = make_template()
    _ = make_node(template, 'right')
    _ = make_block(template, 'wrong')
    node3 = make_block(template, 'right')
    rendering = make_rendering([template])

    assert rendering.block('right') == [node3]
