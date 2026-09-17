#!/usr/bin/env python3
"""Pretty-print an XML file in place (adds newlines/indentation, and wraps
tags with 2+ attributes to one-attribute-per-line if the tag would otherwise
be too wide) so it diffs cleanly. Uses only the standard library
(xml.dom.minidom) -- no extra deps.

Usage: prettify-xml.py <file.xml> [file2.xml ...]
"""
import sys
import xml.dom.minidom

import xml_format


def prettify(path):
    dom = xml.dom.minidom.parse(path)
    text = xml_format.render_document(dom, wrap_predicate=xml_format.line_would_wrap)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    for path in sys.argv[1:]:
        try:
            prettify(path)
        except Exception as e:
            print(f'skipping {path}: {e}', file=sys.stderr)


if __name__ == '__main__':
    main()
