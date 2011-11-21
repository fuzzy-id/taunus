# -*- coding: utf-8 -*-
from pyramid.response import Response
from pyramid.view import view_config


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
    return {'resource': context,
            'listing': ( ListingEntry(entry, request)
                         for entry in context ), }

@view_config(context='taunus.resources.TextFile',
             renderer='taunus:templates/file.pt')
def view_text_file(context, request):
    return {'resource': context, }

@view_config(context='taunus.resources.VideoFile',
             renderer='taunus:templates/video.pt')
def view_video(context, request):
    video_path = request.resource_url(context, 'actual')
    return {'resource': context, 
            'video_path': video_path, }

@view_config(name='actual', context='taunus.resources.VideoFile')
def serve_video(context, request):
    print 'foo'
    return serve_file(context, request)

@view_config(context='taunus.resources.StdFile')
def serve_file(context, request):
    response = Response(content_type=context.mime)
    response.app_iter = open(context.full_path(), 'rb')
    return response
