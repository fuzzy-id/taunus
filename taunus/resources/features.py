# -*- coding: utf-8 -*-
from pyramid.traversal import resource_path

class Downloadable(object):
    
    icon = 'taunus:static/icons/download.png'

    def __init__(self, request, item):

        self.href = resource_path(item)
        self.icon = request.static_path(self.icon)
    
