import unittest
import os
import datetime

import numpy as np

from gpm_repo import gpm_wrapper

class TestGMPImergWrapper(unittest.TestCase):
    def setUp(self):
        package_dir = os.path.dirname(os.path.dirname(__file__))
        repo_dir = os.path.dirname(package_dir)
        test_dir = os.path.join(repo_dir, 'data', 'gpm_sample_data')
        onefile = os.listdir(test_dir)[0]
        abs_onefile = os.path.join(test_dir, onefile)
        self.gpm = gpm_wrapper.GPMImergeWrapper(abs_onefile)

    def test_start_dt(self):
        self.assertIsInstance(self.gpm.start_dt, datetime.datetime)

    def test_end_dt(self):
        self.assertIsInstance(self.gpm.end_dt, datetime.datetime)

    def test_str_attrib(self):
        self.assertIsInstance(self.gpm.abspath, str)
        self.assertIsInstance(self.gpm.basename, str)
        self.assertTrue(self.gpm.abspath.endswith(self.gpm.basename))

    def test_precipCal(self):
        self.assertIsInstance(self.gpm.precipCal, np.ndarray)
        self.assertEqual(self.gpm.precipCal.shape[0], 3600)
        self.assertEqual(self.gpm.precipCal.dtype, np.float32)
