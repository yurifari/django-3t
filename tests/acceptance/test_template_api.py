from django.template.loader import render_to_string

from d3t.watcher import watch_templates


def test_rendered():
    with watch_templates() as rendered:
        render_to_string('root.html')

    assert rendered.template('root.html')
    assert not rendered.template('unknown.html')


def test_contains():
    with watch_templates() as rendered:
        render_to_string('root.html')

    assert rendered.template('root.html').contains('Top level template')
    assert not rendered.template('root.html').contains('Unknown content')


def test_equals():
    with watch_templates() as rendered:
        render_to_string('fragment.html')

    assert rendered.template('fragment.html').equals('Yay!\n')
    assert not rendered.template('fragment.html').equals('Yay!')


def test_with_context():
    with watch_templates() as rendered:
        render_to_string('fragment.html', {'number': 42, 'type': 'answer'})

    assert rendered.template('fragment.html').with_context({'number': 42, 'type': 'answer'})
    assert rendered.template('fragment.html').with_context({'number': 42})
    assert not rendered.template('fragment.html').with_context({'number': 24})
    assert not rendered.template('fragment.html').with_context({'string': '42'})


def test_any():
    with watch_templates() as rendered:
        render_to_string('root.html')

    assert any(rendered.template('fragment.html').with_context({'orientation': 'portrait'}))
    assert not any(rendered.template('fragment.html').with_context({'orientation': 'none'}))


def test_all():
    with watch_templates() as rendered:
        render_to_string('root.html')

    assert all(rendered.template('fragment.html').with_context({'parent': 'root'}))
    assert not all(rendered.template('fragment.html').with_context({'orientation': 'landscape'}))


def test_len():
    with watch_templates() as rendered:
        render_to_string('root.html')

    assert len(rendered.template('root.html')) == 1
    assert len(rendered.template('fragment.html')) == 3
    assert len(rendered.template('unknown.html')) == 0
