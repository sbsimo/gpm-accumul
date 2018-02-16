import datetime
import os
import glob

import h5py
import numpy as np

from .gpm_wrapper import GPMImergeWrapper
from .credentials import DATADIR


class PrecipCalReader:
    PRECIPCAL_FFORMAT = r'precipitationCal_{0}_E{1}.hdf5'
    DT_FORMAT = PRECIPCAL_FFORMAT[:17] + '%Y%m%d_E%H%M.hdf5'

    @classmethod
    def get_latest_precip_file(cls):
        fname_format = cls.PRECIPCAL_FFORMAT.format('*', '*')
        fabspath_format = os.path.join(DATADIR, fname_format)
        candidates = glob.glob(fabspath_format)
        if len(candidates) > 1:
            raise RuntimeError('More than one precipitationCal file is stored in the datadir. There must be only one')
        return candidates[0]

    @classmethod
    def get_latest(cls):
        return cls(cls.get_latest_precip_file())

    def __init__(self, precip_cal_abspath):
        self.precip_cal_abspath = precip_cal_abspath
        self.precip_cal_fname = os.path.basename(precip_cal_abspath)
        self.end_dt = datetime.datetime.strptime(self.precip_cal_fname, self.DT_FORMAT)

    def get_rain_series(self, lon, lat, duration):
        lon_index = GPMImergeWrapper.get_lon_index(lon)
        lat_index = GPMImergeWrapper.get_lat_index(lat)

        loc_index = lon_index * 10000 + lat_index

        delta_dur = datetime.timedelta(hours=duration)
        delta_meas = datetime.timedelta(minutes=30)
        nof_values = int(delta_dur / delta_meas)

        return self.read_rain_values(loc_index, nof_values)

    def read_rain_values(self, loc_index, nof_values):
        f = h5py.File(self.precip_cal_abspath, 'r')
        true_array = np.nonzero(f['location'][:] == loc_index)[0]
        if true_array.shape[0] != 1:
            f.close()
            raise ValueError('The selected location was not alerted')
        start = f['rain'].shape[0] - nof_values
        hrain = f['rain'][start:, true_array[0]]
        f.close()
        return hrain / 2


if __name__ == '__main__':
    lon = -121.94
    lat = 47.66
    hour = 24

    pcr = PrecipCalReader.get_latest()
    rain = pcr.get_rain_series(lon, lat, hour)
    print(rain.shape)
    print(rain.dtype)

    # should fail
    lat = 25.98
    rain = pcr.get_rain_series(lon, lat, hour)
