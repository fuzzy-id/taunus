import unittest
import tempfile
import shutil
from webtest import TestApp
import taunus
import pprint
import os

class ApplicationStartupTests(unittest.TestCase):
    
    def test_unexistent_directory_raises_error_test(self):
        with self.assertRaises(IOError):
            app = taunus.main({}, root_dir='/non/existing/path/')

    def test_app_is_initialized_via_home(self):
        app = TestApp(taunus.main({}))
        req = app.get('/')
        self.assertIn(os.environ['HOME'], req.body)

class FunctionalTests(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        app = taunus.main({}, root_dir=self.test_dir)
        self.app = TestApp(app)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_view_root(self):
        pass
