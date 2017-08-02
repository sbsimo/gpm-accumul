import os
import datetime
from operator import attrgetter

import numpy as np

from gpm_repo import gpm_wrapper

class PrecipTimeSerie():
    """handle and manage a time serie of precipitation data"""

    MEAS_DURATION = datetime.timedelta(minutes=30)

    def __init__(self, duration, end_dt, datadir):
        self.duration = duration
        self.end_dt = end_dt
        self.datadir = datadir
        self.start_dt = end_dt - duration
        self.exp_nmeas = self.duration // self.MEAS_DURATION
        self.measurements = []
        self.dt_index = None
        self._serie = None
        self._accumul = None

    @property
    def serie(self):
        if self._serie is None:
            self._build_serie()
        return self._serie

    @property
    def accumul(self):
        if self._accumul is None:
            self._accumul = np.around(np.sum(
                    self.serie, axis=0, keepdims=False) / 2, 0).astype(np.int16)
        return self._accumul

    def _build_serie(self):
        for meas_fname in gpm_wrapper.get_gpms(self.datadir):
            meas_abspath = os.path.join(self.datadir, meas_fname)
            gpm_meas = gpm_wrapper.GPMImergeWrapper(meas_abspath)
            if gpm_meas.end_dt <= self.end_dt and \
                            gpm_meas.end_dt > self.start_dt:
                self.measurements.append(gpm_meas)
        if len(self.measurements) != self.exp_nmeas:
            raise ValueError
        self.measurements.sort(key=attrgetter('start_dt'))
        self.dt_index = tuple(measure.start_dt for measure in
                              self.measurements)
        self._serie = np.array([measure.precipCal for measure
                                in self.measurements])
        

