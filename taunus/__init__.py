from pyramid.config import Configurator
from taunus.resources import Root

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=Root, settings=settings)
    config.add_view('taunus.views.my_view',
                    context='taunus:resources.Root',
                    renderer='taunus:templates/mytemplate.pt')
    config.add_static_view('static', 'taunus:static', cache_max_age=3600)
    return config.make_wsgi_app()
