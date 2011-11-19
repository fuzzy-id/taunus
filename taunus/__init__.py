from pyramid.config import Configurator
from taunus.resources import RootDir

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=RootDir, 
                          settings=settings)
    config.add_static_view('static', 'taunus:static', 
                           cache_max_age=3600)
    config.scan(taunus.views)
    return config.make_wsgi_app()
