# -*- coding: utf-8 -*-
from pyramid.view import view_config
import os.path

class ListingEntry(object):
    
    def __init__(self, entry, directory, request):
        self.name = entry
        self.directory = directory
        self.request = request

    def __str__(self):
        if os.path.isdir(os.path.join(self.directory.full_path(), self.name)):
            return '<a href="%s">%s</a>' % (self.request.resource_url(self.directory[self.name]),
                                            self.name)
        return self.name


@view_config(context='taunus.resources.Directory',
             renderer='taunus:templates/directory.pt')
def my_view(context, request):

    listing = [ ListingEntry(entry, context, request)
                for entry in context ] 

    return {'directory': context,
            'listing': listing, }
