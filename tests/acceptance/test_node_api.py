from django.template import Context, Template
from django.template.loader import render_to_string

from d3t.watcher import watch_templates


def test_rendered():
    template = Template(
        '{% load echo from tags %}'
        '{% echo %}'
    )

    with watch_templates() as rendered:
        template.render(Context())

    assert rendered.node('echo')
    assert not rendered.template('unknown')


def test_contains():
    template = Template(
        '{% load echo from tags %}'
        '{% echo "Message from the upside down" %}'
    )

    with watch_templates() as rendered:
        template.render(Context())

    assert rendered.node('echo').contains('Message')
    assert not rendered.node('echo').contains('Unknown content')


def test_equals():
    template = Template(
        '{% load echo from tags %}'
        '{% echo "Message from the upside down" %}'
    )

    with watch_templates() as rendered:
        template.render(Context())

    assert rendered.node('echo').equals('Message from the upside down')
    assert not rendered.node('echo').equals('Message')


def test_with_arguments():
    template = Template(
        '{% load free from tags %}'
        '{% free 42 type="answer" %}'
    )

    with watch_templates() as rendered:
        template.render(Context())

    assert rendered.node('free').with_arguments(42, type='answer')
    assert not rendered.node('free').with_arguments(42)
    assert not rendered.node('free').with_arguments(unknown='value')


def test_within():
    with watch_templates() as rendered:
        render_to_string('root.html')

    assert rendered.node('echo').within('fragment.html')
    assert not rendered.node('echo').within('root.html')


def test_any():
    template = Template(
        '{% load free from tags %}'
        '{% free %}'
        '{% free orientation="landscape" %}'
        '{% free orientation="portrait" %}'
    )

    with watch_templates() as rendered:
        template.render(Context())

    assert any(rendered.node('free').with_arguments(orientation='portrait'))
    assert not any(rendered.node('free').with_arguments(orientation='none'))


def test_all():
    template = Template(
        '{% load free from tags %}'
        '{% free 42 %}'
        '{% free 42 orientation="landscape" %}'
        '{% free 42 orientation="portrait" %}'
    )

    with watch_templates() as rendered:
        template.render(Context())

    assert any(rendered.node('free').with_arguments(42))
    assert not any(rendered.node('free').with_arguments(orientation='landscape'))


def test_len():
    template = Template(
        '{% load free from tags %}'
        '{% free 42 %}'
        '{% free 42 orientation="landscape" %}'
        '{% free 42 orientation="portrait" %}'
    )

    with watch_templates() as rendered:
        template.render(Context())

    assert len(rendered.node('free')) == 3
    assert len(rendered.node('unknown')) == 0
