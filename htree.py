# -*- coding: utf-8 -*-
#
# HTMLTree
#
# An HTML Node Tree toolkit.
#
# --------------------------------------------------------------------
#
# Copyright (c) 2015 by Waylan Limberg. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# *   Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
# *   Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
# *   Neither the name of HTMLTree nor the names of its contributors may be
#     used to endorse or promote products derived from this software without
#     specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY WAYLAN LIMBERG ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL ANY CONTRIBUTORS TO HTMLTree
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# --------------------------------------------------------------------
#
# Parts inspired by ElementTree.
#
# The ElementTree toolkit is Copyright (c) 1999-2007 by Fredrik Lundh
#
# --------------------------------------------------------------------


from __future__ import unicode_literals
import sys
try:
    from html import entities
except ImportError:
    import htmlentitydefs as entities


__version__ = '0.0.1'


__all__ = [
    'Element',
    'Comment',
    'Text',
    'RawText',
    'is_node',
    'is_element',
    'is_text',
    'is_raw_text',
    'is_comment',
    'to_string',
    'to_bytes'
]


if sys.version_info[0] == 3:  # pragma: no cover
    text_type = str
else:                         # pragma: no cover
    text_type = unicode       # noqa


# --------------------------------------------------------------------
# Helpers


HTML_EMPTY = set([
    'area', 'base', 'basefont', 'br', 'col', 'frame', 'hr',
    'img', 'input', 'isindex', 'link', 'meta' 'param'
])

HTML_BLOCK = set([
    'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote',
    'pre', 'table', 'dl', 'ol', 'ul', 'script', 'noscript', 'form',
    'fieldset', 'iframe', 'math', 'hr', 'style', 'li', 'dt', 'dd',
    'thead', 'tbody', 'tr', 'th', 'td', 'section', 'footer',
    'header', 'group', 'figure', 'figcaption', 'aside', 'article',
    'canvas', 'output', 'progress', 'video', 'nav'
])


def is_node(node):
    """
    Returns True is object is a node.
    """
    return isinstance(node, Node)


def is_element(node):
    """
    Returns True if object is an element node.
    """
    return isinstance(node, Element)


def is_text(node, strict=False):
    """
    Returns True if object is a Text node.

    If `strict` is True, the object must not be a subclass.
    """
    if strict:
        return isinstance(node, Text) and node.__class__ is Text
    else:
        return isinstance(node, Text)


def is_raw_text(node):
    """
    Returns True if object is a RawText node.
    """
    return isinstance(node, RawText)


def is_comment(node):
    """
    Returns True if object is a Comment node.
    """
    return isinstance(node, Comment)


def is_entity(node):
    """
    Returns True if object is an Entity node:
    """
    return isinstance(node, Entity)


# --------------------------------------------------------------------
# Nodes

class Node(object):
    """
    Base class for nodes.

    All nodes inherit from this class. Do not use this class directly.

    """
    parent = None

    def __repr__(self):
        return '<{0} node at {1:#x}>'.format(self.__class__.__name__, id(self))

    def next_sibling(self):
        """
        Return the next (one) sibling of this node.

        Returns None if this node has no parent or is the last sibling.

        """
        if self.parent is None:
            return None
        try:
            i = self.parent.index(self)
            return self.parent[i+1]
        except (ValueError, IndexError):
            return None

    def next_siblings(self):
        """
        Return an iterator of all siblings which follow this node.

        """
        if self.parent is None:
            return []
        i = self.parent.index(self)
        return self.parent[i+1:]

    def previous_sibling(self):
        """
        Return the previous (one) sibling of this node.

        Returns None if this node has no parent or is the first sibling.

        """
        if self.parent is None:
            return None
        try:
            i = self.parent.index(self)
            # Prevent returning parent[-1] by checking for i > 0
            return self.parent[i-1] if i > 0 else None
        except (ValueError, IndexError):
            return None

    def previous_siblings(self):
        """
        Return an iterator of all siblings which precede this node.

        """
        if self.parent is None:
            return []
        i = self.parent.index(self)
        return self.parent[:i]

    def iter_ancestors(self):
        """
        Return a tree iterator of all ancestors in document order.

        """
        if self.parent is not None:
            yield self.parent
            for p in self.parent.iter_ancestors():
                yield p


class Comment(Node, text_type):
    """
    Comment node.

    Contains the text of an HTML Comment.

    """


class Text(Node, text_type):
    """
    Text node.

    Contains the text of a text node.

    """


class RawText(Text):
    """
    RawText node.

    Contains the text of a raw text node, which the serializer serializes
    as raw text. Be warned that no escaping of any kind is done to raw text.

    """

class Entity(Node, text_type):
    """
    Entity Node.

    Contains a single HTML Entity. Accepts a single Unicode character, a
    Unicode code point, or an HTML entity name. Renders as an HTML5 entity.

    """
    def __init__(self, obj):
        original = obj
        if isinstance(obj, text_type) and len(obj) == 1:
            # Convert Unicode char to code point
            obj = ord(obj)
        if obj in entities.codepoint2name:
            # Get name of code point
            obj = entities.codepoint2name[obj]
        # Ensure name ends with semicolon
        name =  obj if obj.endswith(';') else obj + ';'
        if name in entities.entitydefs or obj in entities.entitydefs:
            # PY2 does not include semicolon in entitydef names so we also check obj
            super(Entity, self).__init__('&'+name)
        else:
            raise TypeError('{0} is not a valid HTML Entity.'.format(repr(original)))


class Element(Node):
    """
    An HTML Element Node

    An element's length is the number of children (including text nodes).

    The element tag, and attributes must be unicode strings.

    When a child is added, that child's `parent` attribute is assigned
    as a reference to the parent instance. When a child is removed,
    the child's `parent` attribute is set to `None`.

    `tag` is the element name. All additional keyword arguments are element
    attributes. If tag is `None`, only its children will be serialized.

    All text is contained in child Text or RawText nodes. The content of
    RawText nodes will not be escaped when serialized. Therefore, use RawText
    nodes to hold the content of "script" and "style" elements.

    Text and RawText nodes cannot contain any children. Neither can any
    Element nodes with tag names listed in HTML_EMPTY.

    """

    tag = None
    """The element's name."""

    attrib = None
    """Dictionary of the element's attributes."""

    def __init__(self, tag=None, **attrib):
        self.tag = tag
        self.attrib = attrib
        self._children = []

    def copy(self):
        """
        Return a shallow copy of current element.

        Subelements will be shared with the original tree.
        The copied element will be detatched from the tree and have no parent.

        """
        node = self.__class__(self.tag, **self.attrib)
        node[:] = self
        node.parent = None
        return node

    def __len__(self):
        return len(self._children)

    def __getitem__(self, index):
        return self._children[index]

    def __setitem__(self, index, node):
        self._assert_can_contain_children()
        if isinstance(index, slice):
            for n in node:
                self._assert_is_node(n)
                n.parent = self
        else:
            self._assert_is_node(node)
            node.parent = self
        self._children[index] = node

    def __delitem__(self, index):
        if hasattr(self._children[index], 'parent'):
            self._children[index].parent = None
        del self._children[index]

    def __iter__(self):
        return iter(self._children)

    def __contains__(self, node):
        return node in self._children

    def _assert_is_node(self, node):
        if not is_node(node):
            raise TypeError('expected a Node, not {0}'.format(type(node).__name__))

    def _assert_can_contain_children(self):
        if self.tag is not None and self.tag.lower() in HTML_EMPTY:
            raise TypeError(
                '{0} is an "empty" HTML element and cannot accept any children'.format(repr(self))
            )

    def index(self, node):
        """
        Return the index of the given child node.

        """
        return self._children.index(node)

    def append(self, node):
        """
        Add child node to the end of this node's children.

        """
        self._assert_can_contain_children()
        self._assert_is_node(node)
        node.parent = self
        self._children.append(node)

    def extend(self, nodes):
        """
        Append child nodes from a sequence to end of this node's children.

        """
        self._assert_can_contain_children()
        for node in nodes:
            self._assert_is_node(node)
            node.parent = self
        self._children.extend(nodes)

    def insert(self, index, node):
        """
        Insert child node at index.

        """
        self._assert_can_contain_children()
        self._assert_is_node(node)
        node.parent = self
        self._children.insert(index, node)

    def remove(self, node):
        """
        Remove matching child node.

        ValueError is raised if a matching node could not be found.

        """
        if hasattr(node, 'parent'):
            node.parent = None
        self._children.remove(node)

    def clear(self):
        """
        Reset Node. Remove all children and clear all attributes.

        """
        self.attrib.clear()
        # Detach parent from each child
        for child in self._children:
            self.remove(child)

    def get(self, key, default=None):
        """
        Get attribute of node or default.

        """
        return self.attrib.get(key, default)

    def set(self, key, value):
        """
        Set attribute of node.

        """
        self.attrib[key] = value

    def keys(self):
        """
        Get list of attribute names.

        """
        return self.attrib.keys()

    def items(self):
        """
        Get element attributes as a list of (name, value) pairs.

        """
        return self.attrib.items()

    def add_class(self, value):
        """
        Add a class name to the `class` attribute.

        """
        value = ' '.join([self.get('class', ''), value]).strip()
        self.set('class', value)

    def remove_class(self, value):
        """
        Remove a class name from the `class` attribute.

        """
        classes = self.get('class', '').split()
        if value in classes:
            classes.remove(value)
            self.set('class', ' '.join(classes).strip())

    def iter_decendents(self, tags=None):
        """
        Return a tree iterator of this node and all decedents in document order.

        `tags` is a sequence of tag names of nodes which will be returned.
        If `tags` is empty (the default), all nodes will be returned.

        """
        tags = tags or []
        if len(tags) == 0 or self.tag in tags:
            yield self
        for c in self._children:
            for gc in c.iter_decendents(tags):
                yield gc

    def iter_text(self, raw=False):
        """
        Return a tree iterator of all decedent text nodes in document order.

        Set `raw` to `True` to include RawText nodes.

        """
        for child in self:
            if is_raw_text(child) and not raw:
                continue
            if is_text(child):
                yield child
            elif is_element(child):
                for gc in child.iter_text():
                    yield gc


# --------------------------------------------------------------------
# Serialization


def _raise_serialization_error(text):
    raise TypeError(
        'cannot serialize {0} (type {1})'.format(repr(text), type(text).__name__)
    )


def _newline_required(node, start=False):
    tag = node.tag.lower()
    if start:
        # This is a start tag
        if tag in HTML_BLOCK and tag not in HTML_EMPTY:
            if tag in ['p', 'P']:
                return False
            if len(node) < 1:
                return False
            return True
        return False
    else:
        # This is an end tag
        if tag in HTML_BLOCK:
            return True
        if tag == 'br':
            return True
        if tag == 'img' and (node.parent is None or node.parent.tag not in ['p', 'P']):
            return True
        return False


def _escape_cdata(text):
    # escape character data
    try:
        # it's worth avoiding do-nothing calls for strings that are
        # shorter than 500 character, or so.  assume that's, by far,
        # the most common case in most applications.
        if '&' in text:
            text = text.replace('&', '&amp;')
        if '<' in text:
            text = text.replace('<', '&lt;')
        if '>' in text:
            text = text.replace('>', '&gt;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)


def _escape_attrib(text):
    # escape attribute value
    try:
        if '&' in text:
            text = text.replace('&', '&amp;')
        if '<' in text:
            text = text.replace('<', '&lt;')
        if '>' in text:
            text = text.replace('>', '&gt;')
        if '"' in text:
            text = text.replace('"', '&quot;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)


def _serialize_node(write, node, format):
    if is_comment(node):
        write('<!-- {0} -->'.format(_escape_cdata(node)))
    elif is_raw_text(node) or is_entity(node):
        write(node)
    elif is_text(node):
        write(_escape_cdata(node))
    elif is_node(node):
        tag = node.tag
        if tag is None:
            for n in node:
                _serialize_node(write, n, format)
        else:
            write('<{0}'.format(tag))
            attribs = sorted(node.items())  # lexical order
            for k, v in attribs:
                v = _escape_attrib(v)
                if k == v and format == 'html':
                    # handle boolean attributes
                    write(' {0}'.format(v))
                else:
                    write(' {0}="{1}"'.format(k, v))
            if format == 'xhtml' and tag.lower() in HTML_EMPTY:
                write(' />')
            else:
                write('>')
                if _newline_required(node, start=True):
                    write('\n')
                if tag.lower() not in HTML_EMPTY:
                    for n in node:
                        _serialize_node(write, n, format)
                    write('</{0}>'.format(tag))
            if _newline_required(node):
                write('\n')
    else:
        _raise_serialization_error(node)


def to_string(node, format='html'):
    """
    Return a serialized unicode string of a node and its children.

    `format` may be one of "html" or "xhtml".
    """
    data = []
    write = data.append
    _serialize_node(write, node, format)
    return "".join(data)


def to_bytes(node, format='html', encoding='utf-8'):
    """
    Return a serialized byte string of a node and its children.

    `format` may be one of "html" or "xhtml".

    `encoding` defaults to utf-8.
    """
    return to_string(node, format).encode(encoding, "xmlcharrefreplace")
