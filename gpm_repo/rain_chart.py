import datetime
import os
import glob
import re

import h5py
import numpy as np

from gpm_repo import utils
from .gpm_wrapper import GPMImergeWrapper
from .time_serie import AlertDetector
from .credentials import DATADIR


class PrecipCalBuilder:

    @staticmethod
    def delete_old():
        fname_format = PrecipCalReader.PRECIPCAL_FFORMAT.format('*', '*')
        fabspath_format = os.path.join(DATADIR, fname_format)
        candidates = glob.glob(fabspath_format)
        candidates.sort()
        for abspath in candidates[:-1]:
            print('Removing old precipCal hdf5 file: ' + abspath)
            os.remove(abspath)

    def __init__(self, serie_obj):
        self.serie_obj = serie_obj
        self._precip_cal = None
        self._alert_locations = None
        self._alerts_abspaths = []
        self._combined_alerts = None

    @property
    def precip_cal(self):
        if self._precip_cal is None:
            self.filter_serie()
        return self._precip_cal

    @property
    def alert_locations(self):
        if self._alert_locations is None:
            self.filter_serie()
        return self._alert_locations

    @property
    def alerts_abspaths(self):
        if not self._alerts_abspaths:
            return self.filter_abspaths()
        return self._alerts_abspaths

    @property
    def combined_alerts(self):
        if self._combined_alerts is None:
            return self.combine_alerts()
        return self._combined_alerts

    def combine_alerts(self):
        combined_alerts = 0
        for abspath in self.alerts_abspaths:
            combined_alerts = combined_alerts + utils.tiff2array(abspath)
        self._combined_alerts = combined_alerts.T
        return self._combined_alerts

    def filter_abspaths(self):
        duration_pattern = AlertDetector.TIF_BASENAME.replace('{:03d}', '(?P<hours>\d{3,3})')
        hours_re = re.compile(duration_pattern)
        alerts_basename = AlertDetector.TIF_BASENAME.replace('{:03d}', '*')
        alerts_abspath = os.path.join(DATADIR, alerts_basename)

        filtered_abspath = []
        for alerts_apath in glob.glob(alerts_abspath):
            m = hours_re.search(alerts_apath)
            hours = int(m.group('hours'))
            if datetime.timedelta(hours=hours) <= self.serie_obj.duration:
                filtered_abspath.append(alerts_apath)

        self._alerts_abspaths = filtered_abspath
        return self._alerts_abspaths

    def filter_serie(self):
        alert_indexes = self.combined_alerts.nonzero()
        all_rain_data = self.serie_obj.serie
        rainoi = all_rain_data[:, alert_indexes[0], alert_indexes[1]]
        alert_locations = alert_indexes[0] * 10000 + alert_indexes[1]
        self._precip_cal = rainoi
        self._alert_locations = alert_locations
        return rainoi, alert_locations

    def store_series(self, out_dir=None):
        if out_dir is None:
            out_dir = DATADIR

        date_str = self.serie_obj.end_dt.strftime('%Y%m%d')
        time_str = self.serie_obj.end_dt.strftime('%H%M')
        abs_path = os.path.join(out_dir, PrecipCalReader.PRECIPCAL_FFORMAT.format(date_str, time_str))

        f = h5py.File(abs_path, 'w')
        f.create_dataset('location', data=self.alert_locations)
        f.create_dataset('rain', data=self.precip_cal)
        f.close()
        print('PrecipitationCal hdf5 file was written: ' + abs_path)
        return abs_path


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
