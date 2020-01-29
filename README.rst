Django 3T
#########

.. image:: https://img.shields.io/pypi/v/django-3t
    :alt: PyPI Version
    :target: https://pypi.python.org/pypi/pytest-3t

.. image:: https://img.shields.io/travis/yurifari/django-3t
    :alt: Travis Build
    :target: https://travis-ci.org/yurifari/django-3t

.. image:: https://img.shields.io/codecov/c/github/yurifari/django-3t
    :alt: Code Coverage
    :target: https://codecov.io/gh/yurifari/django-3t

.. image:: https://img.shields.io/github/license/yurifari/django-3t
    :alt: License
    :target: https://github.com/yurifari/django-3t


Django 3T is a Django Template Testing Tool which aims to help developers to write better tests where the Django template engine is involved.

Some of the things you can do with Django 3T include:

- Ensure a specific ``template``, ``node`` or ``block`` is rendered
- Ensure a specific ``template``, ``node`` or ``block`` is rendered a specific amount of times
- Ensure a specific ``template`` is rendered with a specific context subset
- Ensure a specific ``node`` is rendered with specific arguments
- Ensure a specific ``template``, ``node`` or ``block`` results in a specific content or includes it

.. _installation:

Installation
************
::

    pip install django-3t

.. _usage:

Usage
*****
Django 3T uses the ``watch`` context manager to intercept template and node renderings.

Suppose your project implements the following template called ``homepage.html``:

.. code-block:: html

    {% load say_hello from project_tags %}

    <h1>The most useful website ever</h1>

    {% say_hello request.user %}

A test that makes sure your template and template tag are rendered correctly would roughly look like this:

.. code-block:: python

    from django.contrib.auth import get_user_model
    from django.test import Client

    # 1. Import the context manager
    import d3t

    User = get_user_model()

    def test_homepage():
        user = User.objects.get(username='Billy')
        client = Client()
        client.force_login(user)

        # 2. Wrap the code where the rendering happens
        with d3t.watch() as rendered:
            client.get('/')

        # 3. Assert!
        assert rendered.template('homepage.html')
        assert rendered.node('say_hello').with_arguments(user)

The first assertion makes sure the template ``homepage.html`` was rendered, the second assertion makes sure the template tag ``say_hello`` was rendered and it was done using ``user`` as argument.

For a comprehensive list of available methods, check the `API section <api_>`_.

.. _api:

API
***
You can check that a template, node or block has been rendered and that it did under specific conditions

.. _template-api:

Template API
=================
Check that it has been rendered

.. code-block:: python

    rendered.template('template-name.html')

Check that it has been rendered with a specific context subset

.. code-block:: python

    rendered.template('template-name.html').with_context({'answer': 42})

Check that it has been rendered and the output contains a specific string

.. code-block:: python

    rendered.template('template-name.html').contains('content')

Check that it has been rendered and the output equals a specific string

.. code-block:: python

    rendered.template('template-name.html').equals('full content')

.. _node-api:

Node API
=================
Check that it has been rendered

.. code-block:: python

    rendered.node('node_name')

Check that it has been rendered with specific arguments

.. code-block:: python

    rendered.node('node_name').with_arguments(42, type='answer')

Check that it has been rendered and the output contains a specific string

.. code-block:: python

    rendered.node('node_name').contains('content')

Check that it has been rendered and the output equals a specific string

.. code-block:: python

    rendered.node('node_name').equals('full content')

.. _block-api:

Block API
=================
Check that it has been rendered

.. code-block:: python

    rendered.block('block-name')

Check that it has been rendered and the output contains a specific string

.. code-block:: python

    rendered.block('block-name').contains('content')

Check that it has been rendered and the output equals a specific string

.. code-block:: python

    rendered.block('block-name').equals('full content')

.. _handling-multiple-renderings:

Handling multilpe renderings
============================

A template, node or block could be rendered any number of times, Django 3T allows you to take control of this giving support for the ``not`` operator and for the ``len``, ``all`` and ``any`` built-in functions:

Check that a template/node/block has not been rendered

.. code-block:: python

    not rendered.template('template-name.html')

Check that a template/node/block has been rendered a specific amount of times

.. code-block:: python

    len(rendered.node('node_name')) == 3

Check that all the template/node/block renderings happened under a specific condition

.. code-block:: python

    all(rendered.block('block-name').contains('content'))

Check that any of the template/node/block renderings happened under a specific condition

.. code-block:: python

    any(rendered.template('template-name.html').equals('specific content'))

.. _signals:

Signals
*******
template_rendered
=================
``d3t.signals.template_rendered``

This is sent immediately after a template is rendered.

Arguments sent with this signal:

- | **sender**
  | The ``Template`` class.

- | **instance**
  | The actual template instance being rendered.

- | **context**
  | The context used to render the template.

- | **result**
  | The resulting rendered output.

node_rendered
=================
``d3t.signals.node_rendered``

This is sent immediately after a node is rendered.

Arguments sent with this signal:

- | **sender**
  | The ``Node`` class.

- | **instance**
  | The actual node instance being rendered.

- | **result**
  | The resulting rendered output.
