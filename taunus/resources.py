# -*- coding: utf-8 -*-
import os

class RootDirFactory(object):
    
    _default_root = None

    def __new__(cls, request):
        
        if cls._default_root is None:
            return Directory(os.environ['HOME'])
        return Directory(cls._default_root)

    @classmethod
    def set_default_root(cls, default_root):
        if not os.path.isdir(default_root):
            raise IOError("Couldn't find root dir '%s'." % default_root)
        cls._default_root = default_root

class Directory(object):

    __name__ = None
    __parent__ = None

    def __init__(self, dir):
        self.__name__ = dir

    def __str__(self):
        return self.__name__

    def __iter__(self):
        listing = [ x for x in os.listdir(self.__name__) ]
        listing.sort()
        for entry in listing:
            if os.path.isdir(entry):
                pass
