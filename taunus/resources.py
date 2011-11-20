# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPForbidden
import os

class RootDirFactory(object):
    
    _default_root = None

    def __new__(cls, request):
        cls._validate_root()
        return RootDirectory(cls._default_root)

    @classmethod
    def validate_and_set_default_root(cls, default_root):
        cls._default_root = default_root
        cls._validate_root()

    @classmethod
    def _validate_root(cls):
        if not os.path.isabs(cls._default_root):
            raise ValueError("%s is not absolute!" % cls._default_root)
        elif not os.path.isdir(cls._default_root):
            raise ValueError("No such dir: %s" % cls._default_root)
        elif os.path.islink(cls._default_root):
            raise ValueError("%s is a symlink. Exiting!" % cls._default_root)

class Directory(object):

    def __init__(self, dir):
        self.__name__ = dir

    def __str__(self):
        return '%s%s/' % (str(self.__parent__), self.__name__)

    def full_path(self):
        return '/'.join([self.__parent__.full_path(), self.__name__])

    def __iter__(self):
        full_path = self.full_path()
        listing = os.listdir(full_path)
        listing.sort()
        def directory_listing():
            for item in listing:
                if p_valid_entry(os.path.join(full_path, item)):
                    yield item
        return directory_listing()

    def __getitem__(self, entry):
        if os.path.isdir(os.path.join(self.full_path(), entry)):
            child_dir = Directory(entry)
            child_dir.__parent__ = self
            return child_dir
        raise KeyError()

class RootDirectory(Directory):

    __name__ = ''
    __parent__ = None

    def __init__(self, path):
        self.__path__ = path

    def __str__(self):
        return '/'

    def full_path(self):
        return self.__path__

def p_valid_entry(entry_path):
    if os.path.islink(entry_path):
        return False
    return True
