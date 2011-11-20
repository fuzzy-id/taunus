# -*- coding: utf-8 -*-
from pyramid.view import view_config

@view_config(context='taunus.resources.Directory',
             renderer='taunus:templates/directory.pt')
def my_view(context, request):
    return {'directory': context}
