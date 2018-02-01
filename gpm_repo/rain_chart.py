import datetime

import h5py
import numpy as np

TEST_FILEPATH = r'G:\progetti\ITHACA\tribute\gpm-accumul\data\gpm_data\sample_rainoi.hdf5'


def get_rain_serie(lon, lat, duration):
    lon_index = get_lon_index(lon)
    lat_index = get_lat_index(lat)

    loc_index = lon_index * 10000 + lat_index

    delta_dur = datetime.timedelta(hours=duration)
    delta_meas = datetime.timedelta(minutes=30)
    nof_values = int(delta_dur / delta_meas)

    return read_rain_values(TEST_FILEPATH, loc_index, nof_values)


def get_lon_index(lon):
    lons = np.arange(-179.95, 180, 0.1)
    diffs = lon - lons
    abs_diffs = np.absolute(diffs)
    return abs_diffs.argmin()
    

def get_lat_index(lat):
    lats = np.arange(-59.95, 60, 0.1)
    diffs = lat - lats
    abs_diffs = np.absolute(diffs)
    return abs_diffs.argmin()


def read_rain_values(filepath, loc_index, nof_values):
    f = h5py.File(filepath, 'r')
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
    rain = get_rain_serie(lon, lat, hour)
    print(rain.shape)
    print(rain.dtype)

    # should fail
    lat = 25.98
    rain = get_rain_serie(lon, lat, hour)
