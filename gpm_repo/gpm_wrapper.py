import os
import datetime

import h5py


class GPMImergeWrapper:
    """A class wrapper for GPM IMERGE files"""

    SDTFORMAT = '%Y%m%dS%H%M%S'
    EDTFORMAT = '%Y%m%dE%H%M%S'
    
    def __init__(self, abspath):
        self.abspath = abspath
        self.basename = os.path.basename(abspath)
        self.start_dt = None
        self.end_dt = None
        self._precipCal = None
        
        self._set_datetimes()

    @property
    def precipCal(self):
        if self._precipCal is None:
            f = h5py.File(self.abspath, 'r')
            ds = f['/Grid/precipitationCal']
            self._precipCal = ds[:]
            f.close()
        return self._precipCal

    def _set_datetimes(self):
        datetimeinfo = self.basename.split('.')[4]
        sdate, stime, etime = datetimeinfo.split('-')
        naive_start_dt = datetime.datetime.strptime(sdate + stime,
                                                    self.SDTFORMAT)
        naive_end_dt = datetime.datetime.strptime(sdate + etime,
                                                  self.EDTFORMAT)
        self.start_dt = naive_start_dt.replace(tzinfo=datetime.timezone.utc)
        self.end_dt = naive_end_dt.replace(tzinfo=datetime.timezone.utc)
