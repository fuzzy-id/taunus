# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest

from webtest import TestApp

import taunus


class ApplicationStartupTests(unittest.TestCase):
    
    def test_missing_default_root_raises_error(self):
        with self.assertRaises(KeyError):
            app = taunus.main({})

    def test_init_with_unexistent_default_root_raises_error(self):
        with self.assertRaises(ValueError):
            app = taunus.main({}, default_root='/non/existing/path/')

    def test_default_root_not_absolute_raises_error(self):
        with self.assertRaises(ValueError):
            app = taunus.main({}, default_root='~')

    def test_vanished_default_root_raises_error(self):
        test_dir = tempfile.mkdtemp()
        try:
            app = TestApp(taunus.main({}, default_root=test_dir))
        except Exception as e:
            shutil.rmtree(test_dir)
            raise e
        shutil.rmtree(test_dir)
        with self.assertRaises(ValueError):
            app.get('/')
        
class AccessTests(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        app = taunus.main({}, default_root=self.test_dir)
        self.app = TestApp(app)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_accessing_non_existing_path_is_forbidden(self):
        self.app.get('/non/existing/path', status=404)

    def test_symbolic_link_does_not_show_up_in_listing(self):
        os.symlink('/', os.path.join(self.test_dir, 'symlink'))
        resp = self.app.get('/')
        self.assertNotIn('symlink', resp.body)

class BaseTests(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        app = taunus.main({}, default_root=self.test_dir)
        self.app = TestApp(app)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_directory_is_represented_as_root(self):
        resp = self.app.get('/')
        self.assertIn(' / ', resp.body)

    def test_existing_file_in_dir_is_listed(self):
        with open(os.path.join(self.test_dir, 'foo'), 'w'):
            pass
        resp = self.app.get('/')
        self.assertIn('foo', resp.body)
