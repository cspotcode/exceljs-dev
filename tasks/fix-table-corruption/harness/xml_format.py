#!/usr/bin/env python3
"""Shared XML pretty-printing helpers for the table-corruption harness
scripts (prettify-xml.py, reorder-attrs.py). Renders a parsed minidom
document to indented text, optionally wrapping a tag's attributes one per
line when the tag would otherwise render too wide.

Uses only the standard library (xml.dom.minidom) -- no extra deps.
"""

MAX_LINE_LENGTH = 120
INDENT_UNIT = '  '


def _escape_text(value):
    return value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _escape_attr(value):
    return _escape_text(value).replace('"', '&quot;')


def _attr_items(el):
    return [
        (el.attributes.item(i).name, el.attributes.item(i).value)
        for i in range(el.attributes.length)
    ]


def _format_attr(name, value):
    return f'{name}="{_escape_attr(value)}"'


def _start_tag_line(el, indent):
    attrs = ''.join(f' {_format_attr(name, value)}' for name, value in _attr_items(el))
    return f'{indent}<{el.tagName}{attrs}>'


def line_would_wrap(el, indent_level, indent_unit=INDENT_UNIT, max_line_length=MAX_LINE_LENGTH):
    """True if this element has 2+ attributes and its single-line start tag
    (open form, ignoring self-close) would exceed max_line_length at the
    given indent level."""
    if el.attributes.length < 2:
        return False
    indent = indent_unit * indent_level
    return len(_start_tag_line(el, indent)) > max_line_length


def _is_leaf(el):
    """True if this element has no child elements (only text/empty), so it
    can stay on one line the way toprettyxml renders e.g. <v>0</v>."""
    return not any(c.nodeType == c.ELEMENT_NODE for c in el.childNodes)


def render_element(el, indent_level, wrap_predicate, indent_unit=INDENT_UNIT):
    indent = indent_unit * indent_level
    attrs = _attr_items(el)
    wrap = len(attrs) >= 2 and wrap_predicate(el, indent_level)

    lines = []
    if wrap:
        lines.append(f'{indent}<{el.tagName}')
        attr_indent = indent_unit * (indent_level + 1)
        for name, value in attrs:
            lines.append(f'{attr_indent}{_format_attr(name, value)}')
        tag_open_prefix = indent
    else:
        attr_str = ''.join(f' {_format_attr(name, value)}' for name, value in attrs)
        tag_open_prefix = f'{indent}<{el.tagName}{attr_str}'

    if _is_leaf(el):
        if not el.childNodes:
            if wrap:
                lines.append(f'{indent}/>')
            else:
                lines.append(f'{tag_open_prefix}/>')
        else:
            text = _escape_text(''.join(c.data for c in el.childNodes if c.nodeType == c.TEXT_NODE))
            if wrap:
                lines.append(f'{indent}>{text}</{el.tagName}>')
            else:
                lines.append(f'{tag_open_prefix}>{text}</{el.tagName}>')
        return lines

    # has child elements
    if wrap:
        lines.append(f'{indent}>')
    else:
        lines.append(f'{tag_open_prefix}>')

    for child in el.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            lines.extend(render_element(child, indent_level + 1, wrap_predicate, indent_unit))

    lines.append(f'{indent}</{el.tagName}>')
    return lines


def render_document(dom, wrap_predicate=lambda el, indent_level: False, indent_unit=INDENT_UNIT):
    lines = ['<?xml version="1.0" ?>']
    lines.extend(render_element(dom.documentElement, 0, wrap_predicate, indent_unit))
    return '\n'.join(lines) + '\n'
