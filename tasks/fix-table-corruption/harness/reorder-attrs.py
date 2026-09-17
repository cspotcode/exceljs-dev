#!/usr/bin/env python3
"""Reorder XML attributes (and decide attribute-wrapping) in a set of
"roundtrip" files to match what was observed in a corresponding set of
"orig" files, so that diffs between orig and roundtrip aren't cluttered by
meaningless formatting differences (attribute order is not significant per
the XML spec, and neither is whether attributes happen to wrap to one per
line -- both are purely cosmetic).

Elements and attributes are matched by (namespaceURI, localName), not by
literal prefixed name -- <ns1:foo> and <ns2:foo> are the same tag as long as
"ns1" and "ns2" resolve to the same namespace URI, and likewise for
attributes. This is what the XML spec treats as "the same name": the prefix
is just a shorthand for the URI, not part of the tag/attribute's identity.

For each element (namespaceURI, localName) seen anywhere in the orig files,
we record:
  - the order in which attribute (namespaceURI, localName) keys first
    appeared.
  - whether that tag type should wrap to one-attribute-per-line (true if any
    occurrence of the tag in orig would itself wrap under the max-line-length
    rule -- see xml_format.line_would_wrap).

When reordering/re-wrapping a roundtrip file:
  - if the element was seen in orig, known attributes are placed in the
    captured order (using the roundtrip file's own literal attribute name/
    prefix); any attributes not seen in orig are appended in alphabetical
    order (by literal name). Wrapping follows orig's captured decision for
    that tag type, regardless of roundtrip's own line length.
  - if the element was never seen in orig, its attributes are sorted
    alphabetically (by literal name), and wrapping falls back to the normal
    per-line length rule (there's no orig data to defer to).

Orig files are left untouched -- only roundtrip files are rewritten.

Usage: reorder-attrs.py <origDir> <roundtripDir>
"""
import sys
import xml.dom.minidom

import xml_format


def iter_elements(node):
    if node.nodeType == node.ELEMENT_NODE:
        yield node
    for child in node.childNodes:
        yield from iter_elements(child)


def element_key(el):
    return (el.namespaceURI, el.localName)


def attr_items(el):
    # (attrNode.name, (namespaceURI, localName)) for every attribute, in
    # document order.
    items = []
    for i in range(el.attributes.length):
        a = el.attributes.item(i)
        items.append((a.name, (a.namespaceURI, a.localName)))
    return items


def capture_order(path, order_by_element, wrap_by_element):
    dom = xml.dom.minidom.parse(str(path))
    depth_by_node = {}

    def depth_of(el):
        if el in depth_by_node:
            return depth_by_node[el]
        d = 0
        node = el
        while node.parentNode is not None:
            d += 1
            node = node.parentNode
        depth_by_node[el] = d
        return d

    for el in iter_elements(dom.documentElement):
        key = element_key(el)
        order = order_by_element.setdefault(key, [])
        for _name, attr_key in attr_items(el):
            if attr_key not in order:
                order.append(attr_key)

        if xml_format.line_would_wrap(el, depth_of(el)):
            wrap_by_element[key] = True
        else:
            wrap_by_element.setdefault(key, False)


def reorder_attrs(el, order_by_element):
    """Reorder el's attributes in place to match order_by_element (falling
    back to alphabetical for unknown attributes/elements). Returns True if
    anything changed."""
    current = attr_items(el)
    if len(current) < 2:
        return False

    key_to_name = dict((key, name) for name, key in current)
    current_keys = [key for _name, key in current]

    known_order = order_by_element.get(element_key(el))
    if known_order:
        known = [k for k in known_order if k in current_keys]
        unknown = sorted(
            (k for k in current_keys if k not in known_order),
            key=lambda k: key_to_name[k],
        )
        new_key_order = known + unknown
    else:
        new_key_order = sorted(current_keys, key=lambda k: key_to_name[k])

    new_name_order = [key_to_name[k] for k in new_key_order]
    current_names = [name for name, _key in current]
    if new_name_order == current_names:
        return False

    values = {name: el.getAttribute(name) for name in current_names}
    for name in current_names:
        el.removeAttribute(name)
    for name in new_name_order:
        el.setAttribute(name, values[name])
    return True


def reorder_file(path, order_by_element, wrap_by_element):
    dom = xml.dom.minidom.parse(str(path))
    for el in iter_elements(dom.documentElement):
        reorder_attrs(el, order_by_element)

    def wrap_predicate(el, indent_level):
        key = element_key(el)
        if key in wrap_by_element:
            return wrap_by_element[key]
        return xml_format.line_would_wrap(el, indent_level)

    text = xml_format.render_document(dom, wrap_predicate=wrap_predicate)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    import pathlib

    orig_dir = pathlib.Path(sys.argv[1])
    roundtrip_dir = pathlib.Path(sys.argv[2])

    orig_files = list(orig_dir.rglob('*.xml')) + list(orig_dir.rglob('*.rels'))

    order_by_element = {}
    wrap_by_element = {}
    for path in orig_files:
        try:
            capture_order(path, order_by_element, wrap_by_element)
        except Exception as e:
            print(f'skipping orig {path}: {e}', file=sys.stderr)

    roundtrip_files = list(roundtrip_dir.rglob('*.xml')) + list(roundtrip_dir.rglob('*.rels'))
    for path in roundtrip_files:
        try:
            reorder_file(path, order_by_element, wrap_by_element)
        except Exception as e:
            print(f'skipping roundtrip {path}: {e}', file=sys.stderr)


if __name__ == '__main__':
    main()
