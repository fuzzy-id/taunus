# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest

from webtest import TestApp

import taunus


class ApplicationStartupTests(unittest.TestCase):
    
    def test_init_with_unexistent_default_root_raises_error(self):
        with self.assertRaises(IOError):
            app = taunus.main({}, default_root='/non/existing/path/')

    def test_app_is_initialized_via_home(self):
        app = TestApp(taunus.main({}))
        resp = app.get('/')
        self.assertIn(os.environ['HOME'], resp.body)

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
