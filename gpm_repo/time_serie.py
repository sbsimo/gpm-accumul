import os
import glob
import datetime

import gpm_wrapper

class PrecipTimeSerie():
    """handle and manage a time serie of precipitation data"""

    MEAS_FFORMAT = '3B-HHR-E.MS.MRG.3IMERG.*.RT-H5'
    MEAS_DURATION = datetime.timedelta(minutes=30)

    def __init__(self, duration, end_dt, datadir):
        self.duration = duration
        self.end_dt = end_dt
        self.datadir = datadir
        self.start_dt = end_dt - duration
        self.exp_nmeas = self.duration // self.MEAS_DURATION
        self.measurements = []

    def build_serie(self):
        for meas_abspath in glob.iglob(os.path.join(
                self.datadir, self.MEAS_FFORMAT)):
            gpm_meas = gpm_wrapper.GPMImergeWrapper(meas_abspath)
            if gpm_meas.end_dt <= self.end_dt and \
                            gpm_meas.end_dt > self.start_dt:
                self.measurements.append(gpm_meas)
        if len(self.measurements) != self.exp_nmeas:
            raise ValueError