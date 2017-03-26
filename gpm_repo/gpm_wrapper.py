import os

import h5py


class GPMImergeWrapper:
    """A class wrapper for GPM IMERGE files"""
    def __init__(self, abspath):
        self.abspath = abspath
        self.basename = os.path.basename(abspath)
        # 3B-HHR-E.MS.MRG.3IMERG.20170205-S043000-E045959.0270.V04A
        self.start_date = None
        self.start_time = None
        self.stop_time = None
        self._precipCal = None

    @property
    def precipCal(self):
        if self._precipCal is None:
            f = h5py.File(self.abspath, 'r')
            ds = f['/Grid/precipitationCal']
            self._precipCal = ds[:]
            f.close()
        return self._precipCal

