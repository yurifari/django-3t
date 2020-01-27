import pytest

from d3t.selections import NodeSelection, Selection, TemplateSelection


@pytest.fixture
def make_item(mocker):
    def inner(result):
        mock = mocker.Mock()
        mock.result = result
        mock.__str__ = mocker.Mock(return_value=result)
        return mock
    return inner


@pytest.fixture
def green(make_item):
    return make_item('green')


@pytest.fixture
def yellow(make_item):
    return make_item('yellow')


@pytest.fixture
def orange(make_item):
    return make_item('orange')


@pytest.fixture
def template(make_item):
    item = make_item('template')
    item.name = 'root.html'
    item.context = {'number': 42, 'type': 'answer'}
    return item


@pytest.fixture
def node(make_item, template):
    item = make_item('node')
    item.template = template
    item.arguments = ((42, ), {'type': 'answer'})
    return item


@pytest.fixture
def selection(green, yellow, orange):
    return Selection([green, yellow, orange])


def test_len(selection):
    assert len(selection) == 3


def test_any(orange):
    assert any(Selection([None, orange, None]))
    assert not any(Selection([None, None]))


def test_all(selection, green):
    assert all(selection)
    assert not all(Selection([None, green]))


def test_bool(selection):
    assert selection
    assert not Selection()


def test_str(selection):
    assert str(selection) == "['green', 'yellow', 'orange']"


def test_filter(selection, green, yellow, orange):
    assert selection.filter(lambda item: True) == [green, yellow, orange]
    assert selection.filter(lambda item: False) == [None, None, None]
    assert selection.filter(lambda item: item == yellow) == [None, yellow, None]


def test_contains(selection):
    assert selection.contains('e')
    assert not selection.contains('z')


def test_equals(green, yellow):
    assert Selection([green]).equals('green')
    assert not Selection([yellow]).equals('green')


def test_template_with_context(template):
    assert TemplateSelection([template]).with_context({'number': 42, 'type': 'answer'})
    assert TemplateSelection([template]).with_context({'number': 42})
    assert not TemplateSelection([template]).with_context({'number': 24})
    assert not TemplateSelection([template]).with_context({'letter': 'O'})


def test_node_within(node):
    assert NodeSelection([node]).within('root.html')
    assert not NodeSelection([node]).within('toor.html')


def test_node_with_arguments(node):
    assert NodeSelection([node]).with_arguments(42, type='answer')
    assert not NodeSelection([node]).with_arguments(42)
    assert not NodeSelection([node]).with_arguments(24)
