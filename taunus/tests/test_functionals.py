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

    def test_default_root_is_symlink_raises_error(self):
        os.symlink('/', '/tmp/foo')
        try:
            with self.assertRaises(ValueError):
                app = taunus.main({}, default_root='/tmp/foo')
        finally:
            os.remove('/tmp/foo')

    def test_vanished_default_root_raises_error(self):
        test_dir = tempfile.mkdtemp()
        app = TestApp(taunus.main({}, default_root=test_dir))
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

    def test_accessing_dot_dot_results_in_root(self):
        resp = self.app.get('/')
        self.assertIn('<title>Taunus - /</title>', resp.body)

class DirectoryTests(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        app = taunus.main({}, default_root=self.test_dir)
        self.app = TestApp(app)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_directory_is_represented_as_root(self):
        resp = self.app.get('/')
        self.assertIn('Taunus - /', resp.body)

    def test_existing_file_in_dir_is_listed(self):
        with open(os.path.join(self.test_dir, 'foo'), 'w'):
            pass
        resp = self.app.get('/')
        self.assertIn('foo', resp.body)

    def test_dot_file_is_hidden(self):
        with open(os.path.join(self.test_dir, '.some_dot_file'), 'w'):
            pass
        resp = self.app.get('/')
        self.assertNotIn('.some_dot_file', resp.body)

    def test_symbolic_link_is_hidden(self):
        os.symlink('/', os.path.join(self.test_dir, 'symlink'))
        resp = self.app.get('/')
        self.assertNotIn('symlink', resp.body)

    def test_subdir_shows_up(self):
        os.mkdir(os.path.join(self.test_dir, 'somedir'))
        resp = self.app.get('/')
        self.assertIn('/somedir', resp.body)

    def test_subdir_is_accessible(self):
        os.mkdir(os.path.join(self.test_dir, 'somedir'))
        resp = self.app.get('/somedir')
        self.assertIn('Taunus - /somedir', resp.body)

    def test_file_in_subdir_shows_up(self):
        somedir = os.path.join(self.test_dir, 'somedir')
        os.mkdir(somedir)
        with open(os.path.join(somedir, 'file_in_somedir'), 'w'):
            pass
        resp = self.app.get('/somedir')
        self.assertIn('file_in_somedir', resp.body)
