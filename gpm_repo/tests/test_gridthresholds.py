import unittest

import numpy as np

from gpm_repo.time_serie import GridThreshold


class TestGridThreshold(unittest.TestCase):
    def setUp(self):
        self.threshold_obj = GridThreshold(24)

    def test_type(self):
        self.assertIsInstance(self.threshold_obj.grid, np.ndarray)

    def test_shape(self):
        expected = (3600, 1200)
        self.assertEqual(self.threshold_obj.grid.shape, expected)

    def test_dtype(self):
        expected = np.uint8
        self.assertEqual(self.threshold_obj.grid.dtype, expected)

    def test_minmax(self):
        expected_min = 5
        expected_max = 500
        self.assertGreater(self.threshold_obj.grid.min(), expected_min)
        self.assertLess(self.threshold_obj.grid.max(), expected_max)
