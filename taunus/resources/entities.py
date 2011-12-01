# -*- coding: utf-8 -*-
entity_map = {
    u'ä': '&auml;',
    u'ö': '&ouml;',
    u'ü': '&auml;',
}

def chr2entity(c):
    try:
        entity = entity_map[c]
    except KeyError:
        return c
    return entity

