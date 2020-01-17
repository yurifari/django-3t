from django.template.loader import render_to_string

from d3t.watcher import watch_templates


def test_rendered():
    with watch_templates() as rendered:
        render_to_string('root.html')

    assert rendered.block('header')
    assert not rendered.block('unknown')


def test_contains():
    with watch_templates() as rendered:
        render_to_string('root.html')

    assert rendered.block('fragments').contains('Fragments list')
    assert not rendered.block('fragments').contains('Unknown content')


def test_equals():
    with watch_templates() as rendered:
        render_to_string('root.html')

    assert rendered.block('header').equals('<h1>Top level template</h1>')
    assert not rendered.block('header').equals('Top level template')
