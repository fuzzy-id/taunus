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

class FunctionalTests(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        app = taunus.main({}, default_root=self.test_dir)
        self.app = TestApp(app)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_setting_default_dir_works(self):
        resp = self.app.get('/')
        self.assertIn(self.test_dir, resp.body)

    def test_files_in_dir_are_listed(self):
        with open(os.path.join(self.test_dir, 'foo'), 'w'):
            pass
        resp = self.app.get('/')
        self.assertIn('foo', resp.body)
