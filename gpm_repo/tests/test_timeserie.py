import unittest
import datetime
import os

import numpy as np

from gpm_repo import time_serie, gpm_wrapper
from gpm_repo.credentials import DATADIR


class TestTimeSerie(unittest.TestCase):
    def test_build_serie(self):
        gpms = gpm_wrapper.get_gpms(DATADIR)
        gpms.sort()
        duration = datetime.timedelta(hours = (len(gpms) - 2) // 2)
        end_absfile = os.path.join(DATADIR, gpms[-2])
        end_gpmobj = gpm_wrapper.GPMImergeWrapper(end_absfile)
        end_dt = end_gpmobj.end_dt
        ts = time_serie.PrecipTimeSerie(duration, end_dt, DATADIR)
        ts.build_serie()
        self.assertIsInstance(ts.serie, np.ndarray)
        self.assertEqual(ts.serie.shape[0], 2*((len(gpms) - 2) // 2))
        
        
