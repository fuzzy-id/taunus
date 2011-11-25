from pyramid.config import Configurator
from taunus.resources import RootDirFactory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    RootDirFactory.validate_and_set_default_root(settings['default_root'])
    config = Configurator(root_factory=RootDirFactory, 
                          settings=settings)
    config.add_static_view('static', 'taunus:static', 
                           cache_max_age=3600)
    config.add_subscriber('taunus.subscribers.add_base_template',
                          'pyramid.events.BeforRender')
    config.scan('taunus.views')
    return config.make_wsgi_app()
