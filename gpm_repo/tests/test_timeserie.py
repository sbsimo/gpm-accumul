import unittest
import datetime
import os

import gdalconst
import numpy as np

from osgeo import gdal

from .. import time_serie, gpm_wrapper
from ..credentials import DATADIR


class TestTimeSerie(unittest.TestCase):
    def setUp(self):
        self.gpms = gpm_wrapper.get_gpms(DATADIR)
        self.gpms.sort()
        duration = datetime.timedelta(hours = (len(self.gpms) - 2) // 2)
        end_absfile = os.path.join(DATADIR, self.gpms[-2])
        end_gpmobj = gpm_wrapper.GPMImergeWrapper(end_absfile)
        end_dt = end_gpmobj.end_dt
        self.ts = time_serie.PrecipTimeSerie(duration, end_dt, DATADIR)

    def test_build_serie(self):
        self.assertIsInstance(self.ts.serie, np.ndarray)
        self.assertEqual(self.ts.serie.shape[0], 2*((len(self.gpms) - 2) // 2))
        self.assertEqual(self.ts.serie.shape[1], 3600)
        self.assertEqual(self.ts.serie.dtype, np.float32)

    def test_accumul(self):
        self.assertIsInstance(self.ts.accumul, np.ndarray)
        self.assertEqual(self.ts.accumul.shape[0], 3600)
        self.assertEqual(self.ts.accumul.dtype, np.int16)

    def test_tiff(self):
        tif_abspath = os.path.join(DATADIR, 'test.tif')
        self.ts.save_accumul(tif_abspath)
        self.assertTrue(os.path.exists(tif_abspath))

        dataset = gdal.Open(tif_abspath, gdalconst.GA_ReadOnly)
        self.assertIsNotNone(dataset)
        dataset = None