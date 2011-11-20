# -*- coding: utf-8 -*-
from pyramid.view import view_config
import os.path

class ListingEntry(object):
    
    def __init__(self, entry, request):
        self.entry = entry
        self.request = request

    def __str__(self):
        return str(self.entry)

    @property
    def path(self):
        return self.entry.path

@view_config(context='taunus.resources.Directory',
             renderer='taunus:templates/directory.pt')
def view_directory(context, request):

    listing = [ ListingEntry(entry, request)
                for entry in context ] 

    return {'directory': context,
            'listing': listing, }
