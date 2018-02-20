import unittest
import datetime
import os

import numpy as np

from gpm_repo.rain_chart import PrecipCalBuilder
from gpm_repo.time_serie import PrecipTimeSerie
from gpm_repo.credentials import DATADIR

class TestPrecipCalBuilder(unittest.TestCase):
    def setUp(self):
        self.serie_obj = PrecipTimeSerie.latest(datetime.timedelta(hours=48), DATADIR)

    def test_filterabspaths(self):
        obj = PrecipCalBuilder(self.serie_obj)
        alert_abspaths = obj.filter_abspaths()
        self.assertIsInstance(alert_abspaths, list)
        self.assertGreater(len(alert_abspaths), 0)
        self.assertTrue(os.path.isfile(alert_abspaths[0]))

    def test_combinealerts(self):
        obj = PrecipCalBuilder(self.serie_obj)
        result = obj.combine_alerts()
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result.shape), 2)
        max_result = 3 * len(obj.alerts_abspaths)
        min_result = 0
        self.assertGreaterEqual(result.min(), min_result)
        self.assertLessEqual(result.max(), max_result)

    def test_filterserie(self):
        obj = PrecipCalBuilder(self.serie_obj)
        result_rain, result_loc = obj.filter_serie()
        self.assertEqual(len(result_rain.shape), 2)
        self.assertEqual(len(result_loc.shape), 1)
        self.assertEqual(result_rain.shape[1], result_loc.shape[0])
        self.assertEqual(result_rain.shape[0] * 3600 / 2, self.serie_obj.duration.total_seconds())
        if obj.combined_alerts.max() > 0:
            self.assertGreater(result_rain.shape[1], 0)
        else:
            # not sure what happens if no alerts is raised
            self.assertEqual(1, 0)

    def test_storeserie(self):
        obj = PrecipCalBuilder(self.serie_obj)
        result = obj.store_series()
        self.assertTrue(os.path.isfile(result))
