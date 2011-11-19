default_root = None

def root_dir_factory(request):
    pass

class RootDir(object):
    def __init__(self, dir, request):
        self.request = request
