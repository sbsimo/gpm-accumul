import os
import datetime

from gpm_repo.time_serie import PrecipTimeSerie

from gpm_repo.credentials import DATADIR

def cumulate_12h():
    duration = datetime.timedelta(hours=12)
    naive_end_dt = datetime.datetime(2017, 8, 3, 8, 29, 59)
    end_dt = naive_end_dt.replace(tzinfo=datetime.timezone.utc)

    serie_12h = PrecipTimeSerie(duration, end_dt, DATADIR)

    tif_basename = 'precip_12h_s' + \
                   serie_12h.start_dt.isoformat(timespec='minutes')[:-6] + \
                   '_e' + serie_12h.end_dt.isoformat(timespec='minutes')[:-6]\
                   + '.tif'
    tif_basename = tif_basename.replace(':', '')
    tif_basename = tif_basename.replace('-', '')
    tif_abspath = os.path.join(DATADIR, tif_basename)

    serie_12h.save_accumul(tif_abspath)


if __name__ == '__main__':
    cumulate_12h()