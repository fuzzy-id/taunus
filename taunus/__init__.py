from pyramid.config import Configurator
from taunus.resources import root_dir_factory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=root_dir_factory, 
                          settings=settings)
    config.add_static_view('static', 'taunus:static', 
                           cache_max_age=3600)
    import taunus.views
    config.scan(taunus.views)
    return config.make_wsgi_app()
