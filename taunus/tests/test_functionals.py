import unittest
import tempfile
import shutil
from webtest import TestApp

class ApplicationStartupTests(unittest.TestCase):
    
    def unexistent_directory_raises_error_test(self):
        with self.assertRaises(IOError):
            import taunus
            app = taunus.main({}, root='/non/existing/path/')

class FunctionalTests(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        import taunus
        app = taunus.main({'root': self.test_dir, })
        self.app = TestApp(app)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_view_root(self):
        pass
