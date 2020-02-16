import pytest
from django.template.base import NodeList, Variable
from django.template.context import Context
from django.template.loader_tags import ExtendsNode

from d3t.results import RenderedNode, RenderedResult, RenderedTemplate


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
def make_rendered(mocker):
    def inner(templates=None):
        rendered = RenderedResult()
        rendered.templates = templates or []
        return rendered
    return inner


def test_template_links_nodes_to_itself(mocker):
    node = mocker.Mock()
    template = RenderedTemplate(None, None, [node], None, None)

    assert node.set_template.called_with(template)


def test_template_name(mocker):
    obj = mocker.Mock()
    obj.name = 'root.html'
    template = RenderedTemplate(obj, None, [], None, None)

    assert template.name == 'root.html'


def test_template_to_string():
    template = RenderedTemplate(None, None, [], None, 'terrific')

    assert str(template) == 'terrific'


def test_template_equals(mocker):
    obj = mocker.Mock()
    context = mocker.Mock()
    node1 = mocker.Mock()
    node2 = mocker.Mock()
    parent_name = mocker.Mock()
    template = RenderedTemplate(obj, context, [node1, node2], parent_name, None)

    assert template == RenderedTemplate(obj, context, [node1, node2], parent_name, None)
    assert template != RenderedTemplate(obj, context, [node2, node1], parent_name, None)
    assert template != RenderedTemplate(obj, context, [node1], parent_name, None)
    assert template != RenderedTemplate(mocker.Mock(), context, [node1, node2], parent_name, None)
    assert template != RenderedTemplate(obj, mocker.Mock(), [node1, node2], parent_name, None)
    assert template != RenderedTemplate(obj, context, [node1, node2], mocker.Mock(), None)


def test_node_name(mocker):
    obj = mocker.MagicMock()
    obj.token.split_contents = mocker.Mock(return_value=['magic'])
    node = RenderedNode(obj, None)

    assert node.name == 'magic'


def test_node_name_unavailable(mocker):
    obj = mocker.MagicMock()
    obj.token.split_contents = mocker.Mock(side_effect=IndexError)
    node = RenderedNode(obj, None)

    assert node.name is None


def test_node_arguments(mocker):
    obj = mocker.MagicMock()
    obj.get_resolved_arguments = mocker.Mock(return_value=([42], {'type': 'answer'}))
    template = mocker.Mock()
    template.context = {'orientation': 'landscape'}
    node = RenderedNode(obj, None)
    node.template = template

    assert node.arguments == ((42, ), {'type': 'answer'})
    assert node.obj.get_resolved_arguments.called_with(node.template.context)


def test_node_arguments_unavailable(mocker):
    obj = mocker.MagicMock()
    obj.get_resolved_arguments = mocker.Mock(side_effect=AttributeError)
    template = mocker.Mock()
    template.context = {'orientation': 'landscape'}
    node = RenderedNode(obj, None)
    node.template = template

    assert node.arguments == ((), {})


def test_node_to_string():
    node = RenderedNode(None, 'unbelievable')

    assert str(node) == 'unbelievable'


def test_node_equals(mocker):
    obj = mocker.Mock()
    node = RenderedNode(obj, None)

    assert node == RenderedNode(obj, None)
    assert node != RenderedNode(mocker.Mock(), None)


def test_node_set_template(mocker):
    template = mocker.Mock()
    node = RenderedNode(None, None)
    node.set_template(template)

    assert node.template == template


def test_result_parent_name_from_base_template(mocker):
    nodelist = NodeList()
    context = {}
    rendered = RenderedResult()

    parent_name = rendered._get_extended_template_name(nodelist, context)

    assert parent_name is None


def test_result_parent_name_from_child_template(mocker):
    extends_node = ExtendsNode(NodeList(), Variable('extended-template'))
    nodelist = NodeList([extends_node])
    context = {'extended-template': 'parent-name'}
    rendered = RenderedResult()

    parent_name = rendered._get_extended_template_name(nodelist, context)

    assert parent_name == 'parent-name'


def test_result_template_registration(mocker):
    context = {'key': 'value'}
    request_context = Context({})
    request_context.update(context)
    template = mocker.Mock()
    nodes = [mocker.Mock()]
    result = mocker.Mock()
    rendered = RenderedResult()
    rendered.nodes = nodes
    rendered._get_extended_template_name = mocker.Mock(return_value='parent-name')

    rendered.register_template(mocker.ANY, mocker.ANY, template, request_context, result)

    assert rendered._get_extended_template_name.called_with(template.nodelist, context)
    assert rendered.templates == [RenderedTemplate(template, context, nodes, 'parent-name', result)]


def test_result_node_registration(mocker):
    node = mocker.Mock()
    result = mocker.Mock()
    rendered = RenderedResult()

    rendered.register_node(mocker.ANY, mocker.ANY, node, result)

    assert rendered.nodes == [RenderedNode(node, result)]


def test_result_template(make_template, make_rendered):
    template1 = make_template('right')
    template2 = make_template('wrong')
    template3 = make_template('right')
    rendered = make_rendered([template1, template2, template3])

    assert rendered.template('right') == [template1, template3]


def test_result_node(make_template, make_node, make_rendered):
    template = make_template()
    node1 = make_node(template, 'right')
    _ = make_node(template, 'wrong')
    node3 = make_node(template, 'right')
    rendered = make_rendered([template])

    assert rendered.node('right') == [node1, node3]


def test_result_block(make_node, make_block, make_template, make_rendered):
    template = make_template()
    _ = make_node(template, 'right')
    _ = make_block(template, 'wrong')
    node3 = make_block(template, 'right')
    rendered = make_rendered([template])

    assert rendered.block('right') == [node3]
