"""assignment6-errors/xml_render.py
C3: Render JSON-serialisable data as XML for Accept: application/xml.
"""
from xml.etree.ElementTree import Element, SubElement, tostring


def _build(parent, tag, value):
    if isinstance(value, dict):
        elem = SubElement(parent, tag)
        for k, v in value.items():
            safe = str(k).replace(" ", "_")
            _build(elem, safe, v)
    elif isinstance(value, list):
        elem = SubElement(parent, tag)
        for item in value:
            _build(elem, "item", item)
    else:
        elem = SubElement(parent, tag)
        elem.text = "" if value is None else str(value)


def to_xml(root_tag, data):
    root = Element(root_tag)
    if isinstance(data, dict):
        for k, v in data.items():
            _build(root, str(k).replace(" ", "_"), v)
    else:
        _build(root, "value", data)
    return b'<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(root)
