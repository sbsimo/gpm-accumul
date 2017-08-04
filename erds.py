import glob
import os
import datetime

from gpm_repo.credentials import DATADIR
from gpm_repo.gpm_ftp import GPMFTP
from gpm_repo.gpm_wrapper import GPM_FFORMAT
from gpm_repo.time_serie import PrecipTimeSerie


def mirror_gpm_site():
    # since the maximum cumulate is 144h, we need 288 files to build it
    n_gpm_files = 288
    with GPMFTP() as ftp:
        ftp.grab_latest_nfiles(n_gpm_files, DATADIR)
    # delete old files
    gpm_filelist = glob.glob(os.path.join(DATADIR, GPM_FFORMAT))
    if len(gpm_filelist) > n_gpm_files:
        for gpm_file in gpm_filelist[: n_gpm_files]:
            try:
                os.remove(gpm_file)
            except OSError:
                print('Cannot remove old gpm file: ' + gpm_file)


def compare_dates():
    pass


def compare_precip():
    pass


def cumulate():
    TIFF_FFORMAT = 'precip{:03d}.tif'

    duration = datetime.timedelta(hours=12)
    serie_012h = PrecipTimeSerie.latest(duration, DATADIR)

    tif_abspath = os.path.join(DATADIR, TIFF_FFORMAT.format('12'))
    serie_012h.save_accumul(tif_abspath)

    update_abspath = os.path.join(DATADIR, 'update.txt')
    if serie_012h.measurements:
        with open(update_abspath, 'w') as update_file:
            update_file.write('latest measure ended at:\\n')
            update_file.write(
                serie_012h.measurements[-1].end_dt.isoformat(
                    timespec='minutes'))


def generate_alerts():
    cumulate()
    compare_precip()


def start():
    mirror_gpm_site()
    compare_dates()
    generate_alerts()
