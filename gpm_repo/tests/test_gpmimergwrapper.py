import unittest
import os
import datetime

from gpm_repo import gpm_wrapper

class TestGMPImergWrapper(unittest.TestCase):
    def test_start_dt(self):
        package_dir = os.path.dirname(os.path.dirname(__file__))
        repo_dir = os.path.dirname(package_dir)
        test_dir = os.path.join(repo_dir, 'data', 'gpm_sample_data')
        onefile = os.listdir(test_dir)[0]
        abspath = os.path.abspath(onefile)
        gpm = gpm_wrapper.GPMImergeWrapper(onefile)
        self.assertIsInstance(gpm.start_dt, datetime.datetime)
