========
HTMLTree
========

.. default-role:: code

An HTML Node Tree toolkit.

A Python 2 and 3 library for creating HTML Node Tree objects. While similar to ElementTree
in some respects, it is specifically designed from the ground up for HTML and does not
follow many of ElementTree's XML specific patterns. For example, all text is represented
as child nodes, rather than special `text` and `tail` attributes of Element nodes.
This is a much more natural way of working with HTML and text as elements are more likely
to be interspersed within an element. That said, it is not a Python implementation of
JavaScript's DOM, nor is it trying to be.

Installation
------------

To install HTMLTree run the following command::

    pip install https://github.com/waylan/HTMLTree/archive/master.zip

Note that this is currently **alpha** software and not yet hosted on PyPI. As such, the
above command downloads the source code from GitHub. Upon a stable release, the package will
become available from PyPI.

Usage
-----

To create a node tree, simply start by creating the parent element as an `Element`
instance::

    >>> from htree import Element
    >>> p = Element('p', id='awesome')

Then add some children. First a text node::

    >>> from htree import Text
    >>> ptext = Text('This is ')
    >>> p.append(ptext)

And then some child Elements::

    >>> em = Element('em')
    >>> em.append(Text('really '))
    >>> strong = Element('strong')
    >>> strong.append(Text(awesome))
    >>> em.append(strong)
    >>> p.append(em)
    >>> p.append(Text('!')

Let's see what that looks like when serialized to a string::

    >>> from htree import to_string
    >>> to_string(p)
    '<p id="awesome">This is <em>really <strong>awesome</strong></em>!</p>\n`

You can serialize any node within the tree::

    >>> to_string(strong)
    '<strong>awesome</strong>

Every Node (including Text nodes) contains a reference to its parent::

    >>> strong.parent == em
    True
    >>> ptext.parent == p
    True

There is no special document object. However, if you would like a container
which holds multiple children, but do not want the parent to be an Element,
then create an Element with its tag set to `None`::

    >>> container = Element(None)
    >>> section1 = Element('div', id='section-1')
    >>> section2 = Element('div', id='section-2')
    >>> container.extend([section1, section2])
    >>> to_string(container)
    '<div id="section-1"></div>\n<div id="section-2"></div>\n'

Children can be accessed as nested lists. For Example, determine the number of child
nodes (including text nodes) an Element has by checking its length::

    >>> len(container)
    2

You can iterate over the children::

    >>> for child in container:
    >>>     child.append(p.copy())
    >>>
    >>> print(to_string(container))
    <div id="section-1">
    <p id="awesome">This is <em>really <strong>awesome</strong></em>!</p>
    </div>
    <div id="section-2">
    <p id="awesome">This is <em>really <strong>awesome</strong></em>!</p>
    </div>

And children can be accessed by index::

    >>> container[0] == section1
    True

Obtain the attributes set on an Element with `get`::

    >>> section1.get('id')
    'section-1'

And set an element with `set`. Note that the attribute key is also a string so that
attributes (like "class") which use Python reserved words can be used::

    >>> section1.set('class', 'special')
    >>> section1.get('class')
    'special foo'

As a single Element can contain multiple HTML classes, special methods are provided to
add and remove HTML classes::

    >>> section1.add_class('foo')
    >>> section1.get('class')
    'special foo'
    >>> section1.remove_class('special')
    >>> section1.get('class')
    'foo'

Alternatives
------------

- `BeautifulSoup`_ (An HTML Parser and document object toolkit)
- `ElementTree`_ (A XML Parser and Node Tree toolkit)
- `lxml`_ (XML and HTML toolkit which mostly mirrors ElementTree)
- `AdvancedHTMLParser`_ (A Python clone of the JavaScript DOM API)

.. _`ElementTree`: http://effbot.org/elementtree/ 
.. _`BeautifulSoup`: http://www.crummy.com/software/BeautifulSoup/
.. _`lxml`: http://lxml.de/
.. _`AdvancedHTMLParser`: https://github.com/kata198/AdvancedHTMLParser

Dependencies
------------

HTMLTree is a pure Python library with no external dependencies. It should run without issue
on CPython versions 2.7, 3.3, 3.4, and 3.5 as well as `PyPy`_.

.. _`PyPy`: http://pypy.org/

License
-------

HTMLTree is licensed under the `BSD License`_ as defined in `LICENSE`.

.. _`BSD License`: http://opensource.org/licenses/BSD-2-Clause
