import datetime

import numpy as np
import h5py

from gpm_repo.time_serie import PrecipTimeSerie
from gpm_repo.utils import tiff2array


DATADIR = r'G:\progetti\ITHACA\tribute\gpm-accumul\data\gpm_data'
ALERT_ABSPATH = r"G:\progetti\ITHACA\tribute\gpm-accumul\data\gpm_data\alerts_048h.tif"


def extract_serie():

    # read alerts
    alerts = np.fliplr(tiff2array(ALERT_ABSPATH).T)

    print(alerts.shape)

    alert_indexes = alerts.nonzero()
    print(type(alert_indexes))
    print(len(alert_indexes))
    print(alert_indexes[0].shape, alert_indexes[1].shape)

    # build serie
    duration = datetime.timedelta(hours=72)
    serie = PrecipTimeSerie.latest(duration, DATADIR)
    rain_data = serie.serie
    print(rain_data.shape)
    print(rain_data.size)
    print(rain_data.dtype)
    rainoi = rain_data[:, alert_indexes[0], alert_indexes[1]]
    print(rainoi.shape)
    print(rainoi.size)
    print(rainoi.dtype)

    # build array of index
    location = alert_indexes[0] * 10000 + alert_indexes[1]
    print(location.shape)

    f = h5py.File(r'G:\progetti\ITHACA\tribute\gpm-accumul\data\gpm_data\sample_rainoi.hdf5', 'w')
    f.create_dataset('location', data=location)
    f.create_dataset('rain', data=rainoi)
    f.close()


if __name__ == '__main__':
    extract_serie()