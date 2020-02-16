from django.template.loader import render_to_string

import d3t


def test_rendered():
    with d3t.watch() as rendered:
        render_to_string('root.html')

    assert rendered.template('root.html')
    assert not rendered.template('unknown.html')


def test_contains():
    with d3t.watch() as rendered:
        render_to_string('root.html')

    assert rendered.template('root.html').contains('Top level template')
    assert not rendered.template('root.html').contains('Unknown content')


def test_equals():
    with d3t.watch() as rendered:
        render_to_string('fragment.html')

    assert rendered.template('fragment.html').equals('Yay!\n')
    assert not rendered.template('fragment.html').equals('Yay!')


def test_with_context():
    with d3t.watch() as rendered:
        render_to_string('fragment.html', {'number': 42, 'type': 'answer'})

    assert rendered.template('fragment.html').with_context({'number': 42, 'type': 'answer'})
    assert rendered.template('fragment.html').with_context({'number': 42})
    assert not rendered.template('fragment.html').with_context({'number': 24})
    assert not rendered.template('fragment.html').with_context({'string': '42'})


def test_extends():
    with d3t.watch() as rendered:
        render_to_string('welcome.html')

    assert rendered.template('welcome.html').extends('root.html')
    assert not rendered.template('welcome.html').extends('unknown.html')


def test_any():
    with d3t.watch() as rendered:
        render_to_string('root.html')

    assert any(rendered.template('fragment.html').with_context({'orientation': 'portrait'}))
    assert not any(rendered.template('fragment.html').with_context({'orientation': 'none'}))


def test_all():
    with d3t.watch() as rendered:
        render_to_string('root.html')

    assert all(rendered.template('fragment.html').with_context({'parent': 'root'}))
    assert not all(rendered.template('fragment.html').with_context({'orientation': 'landscape'}))


def test_len():
    with d3t.watch() as rendered:
        render_to_string('root.html')

    assert len(rendered.template('root.html')) == 1
    assert len(rendered.template('fragment.html')) == 3
    assert len(rendered.template('unknown.html')) == 0
