import os
from ftplib import FTP

try:
    from credentials import *
except ImportError:
    print('You must define a user and a password')


class GPMFTP(FTP):

    GPM_HOST = 'jsimpson.pps.eosdis.nasa.gov'
    HHR_E_dir = '/NRTPUB/imerg/early/'

    def __init__(self):
        super().__init__(self.GPM_HOST, user, passwd)

    @staticmethod
    def get_latest_fname():
        with GPMFTP() as ftp:
            latst_modify = ''
            dirname = None
            for elm in ftp.mlsd(GPMFTP.HHR_E_dir, ['modify', 'type']):
                if elm[1]['type'] != 'dir':
                    continue
                modify = elm[1]['modify']
                if modify > latst_modify:
                    latst_modify = modify
                    dirname = elm[0]
            print('Latest modified folder is', dirname, 'on', latst_modify)

            absdirname = GPMFTP.HHR_E_dir + dirname
            latest_fname = ''
            for elm in ftp.mlsd(absdirname, ['modify', 'type']):
                if elm[1]['type'] != 'file':
                    continue
                if elm[0] > latest_fname:
                    latest_fname = elm[0]

        print('Latest filename is', latest_fname)
        return latest_fname

    def grab_file(self):
        pass

# https://pythonprogramming.net/ftp-transfers-python-ftplib/
# def grabFile():
#
#     absfilename = os.path.join(local_datadir, filename)
#     print(absfilename)
#     with open(absfilename, 'wb') as localfile:
#         ftp.retrbinary('RETR ' + remote_filename, localfile.write)

if __name__ == '__main__':
    GPMFTP.get_latest_fname()
