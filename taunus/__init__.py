from pyramid.config import Configurator
from taunus.resources import RootDirFactory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    if 'root_dir' in settings:
        RootDirFactory.set_default_root(settings['root_dir'])
    config = Configurator(root_factory=RootDirFactory, 
                          settings=settings)
    config.add_static_view('static', 'taunus:static', 
                           cache_max_age=3600)
    import taunus.views
    config.scan(taunus.views)
    return config.make_wsgi_app()
