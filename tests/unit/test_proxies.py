from d3t.proxies import RenderedNode, RenderedTemplate


def test_template_links_nodes_to_itself(mocker):
    node = mocker.Mock()
    template = RenderedTemplate(None, None, [node], None)

    assert node.set_template.called_with(template)


def test_template_name(mocker):
    obj = mocker.Mock()
    obj.name = 'root.html'
    template = RenderedTemplate(obj, None, [], None)

    assert template.name == 'root.html'


def test_template_to_string():
    template = RenderedTemplate(None, None, [], 'terrific')

    assert str(template) == 'terrific'


def test_template_equals(mocker):
    obj = mocker.Mock()
    context = mocker.Mock()
    node1 = mocker.Mock()
    node2 = mocker.Mock()
    template = RenderedTemplate(obj, context, [node1, node2], None)

    assert template == RenderedTemplate(obj, context, [node1, node2], None)
    assert template != RenderedTemplate(obj, context, [node2, node1], None)
    assert template != RenderedTemplate(obj, context, [node1], None)
    assert template != RenderedTemplate(mocker.Mock(), context, [node1, node2], None)
    assert template != RenderedTemplate(obj, mocker.Mock(), [node1, node2], None)


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
    node.obj.get_resolved_arguments.assert_called_with(node.template.context)


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
