#!/usr/bin/env python

import unittest
import textwrap
import htree


def dedent(text):
    return textwrap.dedent(text).lstrip('\n')


class TestTypes(unittest.TestCase):

    def test_Text_type(self):
        node = htree.Text('some text')
        self.assertTrue(htree.is_node(node))
        self.assertTrue(htree.is_text(node))
        self.assertTrue(htree.is_text(node, strict=True))
        self.assertFalse(htree.is_raw_text(node))
        self.assertFalse(htree.is_comment(node))
        self.assertFalse(htree.is_element(node))
        self.assertTrue(repr(node).startswith('<Text node at '))
        self.assertEqual(node.parent, None)

    def test_RawText_type(self):
        node = htree.RawText('some text')
        self.assertTrue(htree.is_node(node))
        self.assertTrue(htree.is_text(node))
        self.assertFalse(htree.is_text(node, strict=True))
        self.assertTrue(htree.is_raw_text(node))
        self.assertFalse(htree.is_comment(node))
        self.assertFalse(htree.is_element(node))
        self.assertTrue(repr(node).startswith('<RawText node at '))
        self.assertEqual(node.parent, None)

    def test_Text_subclass_type(self):
        class TextSubclass(htree.Text):
            pass
        node = TextSubclass('some text')
        self.assertTrue(isinstance(node, TextSubclass))
        self.assertTrue(htree.is_node(node))
        self.assertTrue(htree.is_text(node))
        self.assertFalse(htree.is_text(node, strict=True))
        self.assertFalse(htree.is_raw_text(node))
        self.assertFalse(htree.is_comment(node))
        self.assertFalse(htree.is_element(node))
        self.assertTrue(repr(node).startswith('<TextSubclass node at '))
        self.assertEqual(node.parent, None)

    def test_Comment_type(self):
        node = htree.Comment('some text')
        self.assertTrue(htree.is_node(node))
        self.assertFalse(htree.is_text(node))
        self.assertFalse(htree.is_text(node, strict=True))
        self.assertFalse(htree.is_raw_text(node))
        self.assertTrue(htree.is_comment(node))
        self.assertFalse(htree.is_element(node))
        self.assertTrue(repr(node).startswith('<Comment node at '))
        self.assertEqual(node.parent, None)

    def test_Element_type(self):
        node = htree.Element()
        self.assertTrue(htree.is_node(node))
        self.assertFalse(htree.is_text(node))
        self.assertFalse(htree.is_text(node, strict=True))
        self.assertFalse(htree.is_raw_text(node))
        self.assertFalse(htree.is_comment(node))
        self.assertTrue(htree.is_element(node))
        self.assertTrue(repr(node).startswith('<Element node at '))
        self.assertEqual(node.parent, None)
        self.assertEqual(node.tag, None)

    def test_non_node(self):
        obj = 'not a node'
        self.assertFalse(htree.is_node(obj))
        self.assertFalse(htree.is_text(obj))
        self.assertFalse(htree.is_text(obj, strict=True))
        self.assertFalse(htree.is_raw_text(obj))
        self.assertFalse(htree.is_comment(obj))
        self.assertFalse(htree.is_element(obj))


class TestElement(unittest.TestCase):

    def test_Element_init(self):
        node = htree.Element('p', id='foo')
        self.assertTrue(htree.is_element(node))
        self.assertEqual(node.tag, 'p')
        self.assertEqual(list(node.items()), [('id', 'foo')])
        self.assertEqual(node[:], [])

    def test_Element_copy(self):
        parent = htree.Element(None)
        node = htree.Element('p', id='foo')
        node.append(htree.Text('some text)'))
        parent.append(node)
        copy = node.copy()
        self.assertNotEqual(id(node), id(copy))
        self.assertTrue(htree.is_element(node))
        self.assertTrue(htree.is_element(copy))
        self.assertEqual(node.tag, copy.tag)
        self.assertEqual(node[:], copy[:])
        self.assertNotEqual(node.parent, copy.parent)
        self.assertEqual(copy.parent, None)
        self.assertEqual(node.parent, parent)
        self.assertEqual(node.items(), copy.items())
        copy.set('class', 'bar')
        self.assertNotEqual(node.items(), copy.items())
        # TODO: test changes to children

    def test_Element_len(self):
        node = htree.Element('p')
        self.assertEqual(len(node), 0)
        node.append(htree.Text('some text'))
        self.assertEqual(len(node), 1)
        node.append(htree.Element('br'))
        self.assertEqual(len(node), 2)
        node.append(htree.Text('more text'))
        self.assertEqual(len(node), 3)

    def test_Element_getter(self):
        node = htree.Element('p')
        text = htree.Text('some text)')
        node.append(text)
        self.assertEqual(node[0], text)

    def test_Element_setter(self):
        node = htree.Element('p')
        text = htree.Text('some text')
        othertext = htree.Text('other text')
        node.append(text)
        self.assertEqual(len(node), 1)
        node[0] = othertext
        self.assertEqual(len(node), 1)
        self.assertEqual(node[:], [othertext])
        self.assertEqual(othertext.parent, node)
        self.assertNotEqual(node[0], text)

    def test_Element_setter_slice(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        text2 = htree.Text('text2')
        node.extend([text1, text2])
        self.assertEqual(len(node), 2)
        text3 = htree.Text('text3')
        text4 = htree.Text('text4')
        node[1:2] = [text3, text4]
        self.assertEqual(len(node), 3)
        self.assertEqual(node[:], [text1, text3, text4])

    def test_Element_setter_errors(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        with self.assertRaises(IndexError):
            node[0] = text1
        with self.assertRaises(TypeError):
            node[0] = None
        emptynode = htree.Element('br')
        with self.assertRaises(TypeError):
            emptynode[0] = text1

    def test_Element_deleter(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        text2 = htree.Text('text2')
        node.extend([text1, text2])
        self.assertEqual(len(node), 2)
        del node[1]
        self.assertEqual(len(node), 1)
        self.assertEqual(text2.parent, None)
        self.assertEqual(text1.parent, node)

    def test_Element_iter_children(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        text2 = htree.Text('text2')
        node.append(text1)
        node.append(text2)
        self.assertEqual([x for x in node], [text1, text2])

    def test_Element_contains(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        node.append(text1)
        self.assertTrue(text1 in node)
        text2 = htree.Text('text2')
        self.assertFalse(text2 in node)

    def test_Element_index(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        node.append(text1)
        text2 = htree.Text('text2')
        node.append(text2)
        self.assertEqual(node.index(text1), 0)
        self.assertEqual(node.index(text2), 1)
        text3 = htree.Text('text3')
        with self.assertRaises(ValueError):
            node.index(text3)

    def test_Element_append(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        node.append(text1)
        self.assertEqual(len(node), 1)
        self.assertEqual(text1.parent, node)
        text2 = htree.Text('text2')
        node.append(text2)
        self.assertEqual(len(node), 2)
        self.assertEqual(text2.parent, node)
        self.assertEqual(node[:], [text1, text2])

    def test_Element_append_errors(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        with self.assertRaises(TypeError):
            node.append(None)
        emptynode = htree.Element('br')
        with self.assertRaises(TypeError):
            emptynode.append(text1)

    def test_Element_extend(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        text2 = htree.Text('text2')
        self.assertEqual(len(node), 0)
        node.extend([text1, text2])
        self.assertEqual(len(node), 2)
        self.assertEqual(text1.parent, node)
        self.assertEqual(text2.parent, node)
        self.assertEqual(node[:], [text1, text2])

    def test_Element_extend_errors(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        with self.assertRaises(TypeError):
            node.extend([None])
        emptynode = htree.Element('br')
        with self.assertRaises(TypeError):
            emptynode.extend([text1])

    def test_Element_insert(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        text2 = htree.Text('text2')
        text3 = htree.Text('text3')
        self.assertEqual(len(node), 0)
        node.insert(0, text1)
        self.assertEqual(len(node), 1)
        node.insert(1, text2)
        self.assertEqual(len(node), 2)
        node.insert(1, text3)
        self.assertEqual(len(node), 3)
        self.assertEqual(node[:], [text1, text3, text2])

    def test_Element_insert_errors(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        with self.assertRaises(TypeError):
            node.insert(None)
        emptynode = htree.Element('br')
        with self.assertRaises(TypeError):
            emptynode.insert(text1)

    def test_Element_remove(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        text2 = htree.Text('text2')
        node.extend([text1, text2])
        self.assertEqual(len(node), 2)
        node.remove(text1)
        self.assertEqual(len(node), 1)
        self.assertEqual(text1.parent, None)
        self.assertEqual(node[:], [text2])

    def test_Element_clear(self):
        node = htree.Element('p', id='foo')
        child = htree.Text('some text)')
        node.append(child)
        node.clear()
        self.assertEqual(node.tag, 'p')
        self.assertEqual(list(node.items()), [])
        self.assertEqual(node[:], [])
        self.assertEqual(child.parent, None)

    def test_Element_next_sibling(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        text2 = htree.Text('text2')
        text3 = htree.Text('text3')
        node.append(text1)
        node.append(text2)
        node.append(text3)
        self.assertEqual(text1.next_sibling(), text2)
        self.assertEqual(text2.next_sibling(), text3)
        self.assertEqual(text3.next_sibling(), None)
        self.assertEqual(node.next_sibling(), None)

    def test_Element_previous_sibling(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        text2 = htree.Text('text2')
        text3 = htree.Text('text3')
        node.append(text1)
        node.append(text2)
        node.append(text3)
        self.assertEqual(text1.previous_sibling(), None)
        self.assertEqual(text2.previous_sibling(), text1)
        self.assertEqual(text3.previous_sibling(), text2)
        self.assertEqual(node.previous_sibling(), None)

    def test_Element_next_siblings(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        text2 = htree.Text('text2')
        text3 = htree.Text('text3')
        node.append(text1)
        node.append(text2)
        node.append(text3)
        self.assertEqual(text1.next_siblings(), [text2, text3])
        self.assertEqual(text2.next_siblings(), [text3])
        self.assertEqual(text3.next_siblings(), [])
        self.assertEqual(node.next_siblings(), [])

    def test_Element_previous_siblings(self):
        node = htree.Element('p')
        text1 = htree.Text('text1')
        text2 = htree.Text('text2')
        text3 = htree.Text('text3')
        node.append(text1)
        node.append(text2)
        node.append(text3)
        self.assertEqual(text1.previous_siblings(), [])
        self.assertEqual(text2.previous_siblings(), [text1])
        self.assertEqual(text3.previous_siblings(), [text1, text2])
        self.assertEqual(node.previous_siblings(), [])

    def test_Element_attrib_get(self):
        node = htree.Element('p', id='foo')
        self.assertEqual(node.get('id'), 'foo')
        self.assertEqual(node.get('missing'), None)
        self.assertEqual(node.get('missing', 'default'), 'default')

    def test_Element_attrib_set(self):
        node = htree.Element('p', id='foo')
        node.set('id', 'bar')
        node.set('class', 'baz')
        self.assertEqual(sorted(node.items()), [('class', 'baz'), ('id', 'bar')])

    def test_Element_attrib_keys(self):
        node = htree.Element('p', **{'id': 'foo', 'class': 'baz'})
        self.assertEqual(sorted(node.keys()), ['class', 'id'])

    def test_Element_attrib_items(self):
        node = htree.Element('p', **{'id': 'foo', 'class': 'baz'})
        self.assertEqual(sorted(node.items()), [('class', 'baz'), ('id', 'foo')])

    def test_Element_attrib_class(self):
        node = htree.Element('p')
        self.assertEqual(node.get('class'), None)
        node.add_class('foo')
        self.assertEqual(node.get('class'), 'foo')
        node.add_class('bar')
        self.assertEqual(node.get('class'), 'foo bar')
        node.add_class('baz')
        self.assertEqual(node.get('class'), 'foo bar baz')
        node.remove_class('bar')
        self.assertEqual(node.get('class'), 'foo baz')
        node.remove_class('missing')
        self.assertEqual(node.get('class'), 'foo baz')

    def test_Element_iter_decendents(self):
        p = htree.Element('p')
        em = htree.Element('em')
        strong = htree.Element('strong')
        a1 = htree.Element('a')
        a2 = htree.Element('a')
        p.append(em)
        em.append(strong)
        strong.append(a1)
        p.append(a2)
        self.assertEqual(list(p.iter_decendents()), [p, em, strong, a1, a2])
        self.assertEqual(list(p.iter_decendents('em')), [em])
        self.assertEqual(list(p.iter_decendents('a')), [a1, a2])
        self.assertEqual(list(p.iter_decendents('br')), [])

    def test_Element_itertext(self):
        p = htree.Element('p')
        ptext = htree.RawText('ptext')
        em = htree.Element('em')
        emtext = htree.Text('emtext')
        strong = htree.Element('strong')
        strongtext = htree.Text('strongtext')
        a1 = htree.Element('a')
        a1text = htree.Text('a1text')
        a2 = htree.Element('a')
        a2text = htree.Text('a2text')
        p.append(ptext)
        p.append(em)
        em.append(emtext)
        em.append(strong)
        strong.append(strongtext)
        strong.append(a1)
        a1.append(a1text)
        p.append(a2)
        a2.append(a2text)
        self.assertEqual(list(p.iter_text()), [emtext, strongtext, a1text, a2text])
        self.assertEqual(
            list(p.iter_text(raw=True)),
            [ptext, emtext, strongtext, a1text, a2text]
        )

    def test_Element_iter_ancestors(self):
        p = htree.Element('p')
        em = htree.Element('em')
        strong = htree.Element('strong')
        a1 = htree.Element('a')
        a2 = htree.Element('a')
        p.append(em)
        em.append(strong)
        strong.append(a1)
        p.append(a2)
        self.assertEqual(list(a1.iter_ancestors()), [strong, em, p])
        self.assertEqual(list(a2.iter_ancestors()), [p])
        self.assertEqual(list(strong.iter_ancestors()), [em, p])


class TestSerializer(unittest.TestCase):

    def test_Text_to_string(self):
        node = htree.Text('some text')
        self.assertEqual(htree.to_string(node), 'some text')
        self.assertEqual(htree.to_string(node, format='xhtml'), 'some text')

    def test_Text_subclass_to_string(self):
        class TextSubclass(htree.Text):
            pass
        node = TextSubclass('some text')
        self.assertEqual(htree.to_string(node), 'some text')
        self.assertEqual(htree.to_string(node, format='xhtml'), 'some text')

    def test_RawText_to_string(self):
        node = htree.RawText('some text')
        self.assertEqual(htree.to_string(node), 'some text')
        self.assertEqual(htree.to_string(node, format='xhtml'), 'some text')

    def test_Comment_to_string(self):
        node = htree.Comment('some text')
        self.assertEqual(htree.to_string(node), '<!-- some text -->')
        self.assertEqual(htree.to_string(node, format='xhtml'), '<!-- some text -->')

    def test_Text_escape_to_string(self):
        node = htree.Text('text & <tag>')
        self.assertEqual(htree.to_string(node), 'text &amp; &lt;tag&gt;')
        self.assertEqual(
            htree.to_string(node, format='xhtml'),
            'text &amp; &lt;tag&gt;'
        )

    def test_Text_subclass_escape_to_string(self):
        class TextSubclass(htree.Text):
            pass
        node = TextSubclass('"text" & <tag>')
        self.assertEqual(htree.to_string(node), '"text" &amp; &lt;tag&gt;')
        self.assertEqual(
            htree.to_string(node, format='xhtml'),
            '"text" &amp; &lt;tag&gt;'
        )

    def test_RawText_escape_to_string(self):
        node = htree.RawText('"text" & <tag>')
        self.assertEqual(htree.to_string(node), '"text" & <tag>')
        self.assertEqual(htree.to_string(node, format='xhtml'), '"text" & <tag>')

    def test_Comment_escape_to_string(self):
        node = htree.Comment('"text" & <tag>')
        self.assertEqual(htree.to_string(node), '<!-- "text" &amp; &lt;tag&gt; -->')
        self.assertEqual(
            htree.to_string(node, format='xhtml'),
            '<!-- "text" &amp; &lt;tag&gt; -->'
        )

    def test_Element_empty_tag_is_None_to_string(self):
        node = htree.Element()
        self.assertEqual(htree.to_string(node), '')
        self.assertEqual(htree.to_string(node, format='xhtml'), '')

    def test_Element_empty_tag_is_empty_to_string(self):
        node = htree.Element('br')
        self.assertEqual(htree.to_string(node), '<br>\n')
        self.assertEqual(htree.to_string(node, format='xhtml'), '<br />\n')

    def test_Element_empty_tag_not_empty_to_string(self):
        node = htree.Element('p')
        self.assertEqual(htree.to_string(node), '<p></p>\n')
        self.assertEqual(htree.to_string(node, format='xhtml'), '<p></p>\n')

    def test_Element_with_text_tag_is_None_to_string(self):
        node = htree.Element()
        node.append(htree.Text('some text'))
        self.assertEqual(htree.to_string(node), 'some text')
        self.assertEqual(htree.to_string(node, format='xhtml'), 'some text')

    def test_Element_with_child_tag_is_None_to_string(self):
        node = htree.Element()
        node.append(htree.Element('p'))
        self.assertEqual(htree.to_string(node), '<p></p>\n')
        self.assertEqual(htree.to_string(node, format='xhtml'), '<p></p>\n')

    def test_Element_with_children_tag_is_None_to_string(self):
        node = htree.Element()
        node.extend([htree.Element('p'), htree.Element('br'), htree.Element('hr')])
        self.assertEqual(htree.to_string(node), dedent(
            '''
            <p></p>
            <br>
            <hr>
            '''
        ))
        self.assertEqual(htree.to_string(node, format='xhtml'), dedent(
            '''
            <p></p>
            <br />
            <hr />
            '''
        ))

    def test_Element_with_text_to_string(self):
        node = htree.Element('p')
        node.append(htree.Text('some text'))
        self.assertEqual(htree.to_string(node), '<p>some text</p>\n')
        self.assertEqual(htree.to_string(node, format='xhtml'), '<p>some text</p>\n')

    def test_Element_with_child_to_string(self):
        node = htree.Element('div')
        node.append(htree.Element('p'))
        self.assertEqual(htree.to_string(node), dedent(
            '''
            <div>
            <p></p>
            </div>
            '''
        ))
        self.assertEqual(htree.to_string(node, format='xhtml'), dedent(
            '''
            <div>
            <p></p>
            </div>
            '''
        ))

    def test_Element_with_children_to_string(self):
        node = htree.Element('div')
        node.extend([htree.Element('div'), htree.Element('hr'), htree.Element('img')])
        self.assertEqual(htree.to_string(node), dedent(
            '''
            <div>
            <div></div>
            <hr>
            <img>
            </div>
            '''
        ))
        self.assertEqual(htree.to_string(node, format='xhtml'), dedent(
            '''
            <div>
            <div></div>
            <hr />
            <img />
            </div>
            '''
        ))

    def test_Element_with_nested_children_to_string(self):
        div = htree.Element('div')
        p = htree.Element('p')
        p.append(htree.Text('Some text '))
        em = htree.Element('em')
        em.append(htree.Text('with emphasis'))
        p.append(em)
        p.append(htree.Text('.'))
        div.append(p)
        self.assertEqual(htree.to_string(div), dedent(
            '''
            <div>
            <p>Some text <em>with emphasis</em>.</p>
            </div>
            '''
        ))
        self.assertEqual(htree.to_string(div, format='xhtml'), dedent(
            '''
            <div>
            <p>Some text <em>with emphasis</em>.</p>
            </div>
            '''
        ))

    def test_Element_with_attr_to_string(self):
        p = htree.Element('p', id='foo')
        img = htree.Element('img', src='example.jpg', alt='An image.')
        p.append(img)
        self.assertEqual(htree.to_string(p), dedent(
            '''
            <p id="foo"><img alt="An image." src="example.jpg"></p>
            '''
        ))
        self.assertEqual(htree.to_string(p, format='xhtml'), dedent(
            '''
            <p id="foo"><img alt="An image." src="example.jpg" /></p>
            '''
        ))

    def test_Element_with_bool_attr_to_string(self):
        inpt = htree.Element('input', checked='checked', disabled='disabled')
        inpt.set('name', 'foo')
        inpt.set('type', 'checkbox')
        self.assertEqual(
            htree.to_string(inpt),
            '<input checked disabled name="foo" type="checkbox">'
        )
        self.assertEqual(
            htree.to_string(inpt, format='xhtml'),
            '<input checked="checked" disabled="disabled" name="foo" type="checkbox" />'
        )

    def test_Element_with_attr_escape_to_string(self):
        img = htree.Element('img', src='example.jpg', alt='"text" & <tag>')
        self.assertEqual(htree.to_string(img), dedent(
            '''
            <img alt="&quot;text&quot; &amp; &lt;tag&gt;" src="example.jpg">
            '''
        ))
        self.assertEqual(htree.to_string(img, format='xhtml'), dedent(
            '''
            <img alt="&quot;text&quot; &amp; &lt;tag&gt;" src="example.jpg" />
            '''
        ))

    def test_Element_with_invalid_attr_to_string(self):
        p = htree.Element('p', id=None)
        self.assertRaises(TypeError, htree.to_string, p)

    def test_invalid_node_to_string(self):
        self.assertRaises(TypeError, htree.to_string, None)

    def test_escape_cdata_invalid(self):
        self.assertRaises(TypeError, htree._escape_cdata, None)


if __name__ == '__main__':
    unittest.main()
