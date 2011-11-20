# -*- coding: utf-8 -*-
import os

class RootDirFactory(object):
    
    _default_root = None

    def __new__(cls, request):
        
        if cls._default_root is None:
            return Directory(os.environ['HOME'])
        return Directory(cls._default_root)

    @classmethod
    def set_default_root(cls, root_dir):
        if not os.path.isdir(root_dir):
            raise IOError("Couldn't find root dir '%s'." % root_dir)


class Directory(object):

    __name__ = None
    __parent__ = None

    def __init__(self, dir):
        self.__name__ = dir

    def __str__(self):
        return self.__name__
