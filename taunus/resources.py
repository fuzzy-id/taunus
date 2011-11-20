# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPForbidden
from pyramid.traversal import resource_path
import os
import re

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

class BaseFSObject(object):
    """
    Defines properties and functions that all objects in the
    file system will share.
    """
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __str__(self):
        return self.__name__

    def full_path(self):
        return '/'.join([self.__parent__.full_path(), self.__name__])

    @property
    def path(self):
        return resource_path(self)
        
class Directory(BaseFSObject):

    def __iter__(self):
        full_path = self.full_path()
        listing = os.listdir(full_path)
        listing.sort()
        def directory_listing():
            for item in listing:
                cls = self.get_entry_type(item)
                if cls is not None:
                    yield cls(self, item)
        return directory_listing()

    def __getitem__(self, entry):
        cls = self.get_entry_type(entry)
        if cls is not None:
            return cls(self, entry)
        raise KeyError()

    def get_entry_type(self, entry):
        entry_path = os.path.join(self.full_path(), entry)
        if not is_valid_entry(entry_path):
            return None
        elif os.path.isdir(entry_path):
            return Directory
        return File

class RootDirectory(Directory):

    __name__ = ''
    __parent__ = None

    def __init__(self, path):
        self.__path__ = path

    def __str__(self):
        return '/'

    def full_path(self):
        return self.__path__

class File(BaseFSObject):
    
    pass

dotfile_re = re.compile(r'^\.([^.]|\..+)')
def is_valid_entry(entry_path):
    if os.path.islink(entry_path):
        return False
    if dotfile_re.match(os.path.basename(entry_path)) is not None:
        return False
    return True
