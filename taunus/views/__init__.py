# -*- coding: utf-8 -*-
from pyramid.location import lineage
from pyramid.response import Response
from pyramid.traversal import resource_path
from pyramid.view import view_config

@view_config(context='taunus.resources.Directory',
             renderer='taunus:templates/directory.pt')
def view_directory(context, request):
    return {'resource': context,
            'root_to_resource': [ (r, resource_path(r), )
                                  for r in reversed(
                [ c for c in lineage(context) ]) ], }

@view_config(context='taunus.resources.StdFile')
def serve_file(context, request):
    response = Response(content_type=context.mime)
    response.app_iter = open(context.full_path(), 'rb')
    return response
