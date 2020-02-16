from django.template.base import NodeList, Template
from django.template.loader_tags import ExtendsNode

from d3t.rendering import defuse_extends_node, render
from d3t.results import RenderedResult


def test_defuse_extends_node_from_base_template(mocker):
    nodelist = NodeList([mocker.MagicMock(), mocker.MagicMock()])
    template = Template('')
    template.nodelist = nodelist

    defuse_extends_node(template)

    assert template.nodelist == nodelist


def test_defuse_extends_node_from_child_template(mocker):
    nodelist = NodeList([mocker.MagicMock(), mocker.MagicMock()])
    extends_node = ExtendsNode(nodelist, mocker.Mock())
    template = Template('')
    template.nodelist = NodeList([extends_node])

    defuse_extends_node(template)

    assert extends_node.render() is None
    assert template.nodelist == NodeList([extends_node] + nodelist)


def test_render(mocker):
    template_name = 'template-name'
    context = {'key': 'value'}
    template = mocker.Mock()
    get_template = mocker.patch('d3t.rendering.get_template', return_value=template)
    defuse_extends_node = mocker.patch('d3t.rendering.defuse_extends_node')

    result = render(template_name, context)

    assert get_template.called_with(template_name, context)
    assert defuse_extends_node.called_with(template.template)
    assert template.render.called_with(context)
    assert isinstance(result, RenderedResult)


def test_render_uses_using(mocker):
    template_name = 'template-name'
    engine = 'engine-name'
    get_template = mocker.patch('d3t.rendering.get_template')

    render(template_name, mocker.Mock, using=engine)

    assert get_template.called_with(template_name, using=engine)
