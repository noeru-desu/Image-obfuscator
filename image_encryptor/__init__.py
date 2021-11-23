'''
Author       : noeru_desu
Date         : 2021-11-12 16:50:59
LastEditors  : noeru_desu
LastEditTime : 2021-11-23 21:13:02
Description  : 全局版本常量
'''
RELEASE = 0
RELEASE_CANDIDATE = 1
BETA = 2
ALPHA = 3
VERSION_TYPE = RELEASE_CANDIDATE
VERSION_NUMBER = '1.0.0'
SUB_VERSION_NUMBER = 'rc.2'
VERSION_BATCH = '20211123-1'
BRANCH = 'dev/1.x'

OPEN_SOURCE_URL = 'https://github.com/noeru-desu/Image-encryptor'

EXTENSION = {
    '.blp': 'BLP', '.bmp': 'BMP', '.dib': 'DIB', '.bufr': 'BUFR', '.cur': 'CUR',
            '.pcx': 'PCX', '.dcx': 'DCX', '.dds': 'DDS', '.ps': 'EPS', '.eps': 'EPS',
            '.fit': 'FITS', '.fits': 'FITS', '.fli': 'FLI', '.flc': 'FLI', '.ftc': 'FTEX',
            '.ftu': 'FTEX', '.gbr': 'GBR', '.gif': 'GIF', '.grib': 'GRIB', '.h5': 'HDF5',
            '.hdf': 'HDF5', '.png': 'PNG', '.apng': 'PNG', '.jp2': 'JPEG2000', '.j2k': 'JPEG2000',
            '.jpc': 'JPEG2000', '.jpf': 'JPEG2000', '.jpx': 'JPEG2000', '.j2c': 'JPEG2000', '.icns': 'ICNS',
            '.ico': 'ICO', '.im': 'IM', '.iim': 'IPTC', '.tif': 'TIFF', '.tiff': 'TIFF',
            '.jfif': 'JPEG', '.jpe': 'JPEG', '.jpg': 'JPEG', '.jpeg': 'JPEG', '.mpg': 'MPEG',
            '.mpeg': 'MPEG', '.mpo': 'MPO', '.msp': 'MSP', '.palm': 'PALM', '.pcd': 'PCD',
            '.pdf': 'PDF', '.pxr': 'PIXAR', '.pbm': 'PPM', '.pgm': 'PPM', '.ppm': 'PPM',
            '.pnm': 'PPM', '.psd': 'PSD', '.bw': 'SGI', '.rgb': 'SGI', '.rgba': 'SGI',
            '.sgi': 'SGI', '.ras': 'SUN', '.tga': 'TGA', '.icb': 'TGA', '.vda': 'TGA',
            '.vst': 'TGA', '.webp': 'WEBP', '.wmf': 'WMF', '.emf': 'WMF', '.xbm': 'XBM',
            '.xpm': 'XPM'
}

EXTENSION_KEYS = (
    'blp', 'bmp', 'dib', 'bufr', 'cur',
    'pcx', 'dcx', 'dds', 'ps', 'eps',
    'fit', 'fits', 'fli', 'flc', 'ftc',
    'ftu', 'gbr', 'gif', 'grib', 'h5',
    'hdf', 'png', 'apng', 'jp2', 'j2k',
    'jpc', 'jpf', 'jpx', 'j2c', 'icns',
    'ico', 'im', 'iim', 'tif', 'tiff',
    'jfif', 'jpe', 'jpg', 'jpeg', 'mpg',
    'mpeg', 'mpo', 'msp', 'palm', 'pcd',
    'pdf', 'pxr', 'pbm', 'pgm', 'ppm',
    'pnm', 'psd', 'bw', 'rgb', 'rgba',
    'sgi', 'ras', 'tga', 'icb', 'vda',
    'vst', 'webp', 'wmf', 'emf', 'xbm',
    'xpm'
)
