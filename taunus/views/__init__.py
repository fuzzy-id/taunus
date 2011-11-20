# -*- coding: utf-8 -*-
from pyramid.view import view_config

@view_config(context='taunus.resources.RootDir',
             renderer='taunus:templates/dir_list.pt')
def my_view(context, request):
    return {'directory': context}
