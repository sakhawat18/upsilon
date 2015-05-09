__author__ = 'kim'

import time

from upsilon.extract_features.extract_features import ExtractFeatures
from upsilon.datasets.base import load_EROS_lc
from upsilon.utils.utils import sigma_clipping_without_error
from upsilon.utils.utils import sigma_clipping
from upsilon.utils.logger import Logger


def run():
    """
    Test UPSILoN package.

    :return: None
    """

    #logger = Logger('/Users/kim/Temp/test.log').getLogger()
    logger = Logger().getLogger()

    date, mag, err = load_EROS_lc()

    index = mag < 99.999
    date = date[index]
    mag = mag[index]
    err = err[index]

    logger.info('Before sigma-clipping: %d data points' % len(date))
    #date, mag, err = sigma_clipping_without_error(date, mag)
    date, mag, err = sigma_clipping(date, mag, err)
    logger.info('After sigma-clipping: %d data points' % len(date))

    for i in range(1):
        start = time.time()
        e_features = ExtractFeatures(date, mag, err)
        end = time.time()
        logger.info('Initializing time: %.4f seconds' % (end - start))

        start = time.time()
        e_features.shallow_run()
        end = time.time()
        logger.info('Shallow-run processing time: %.4f seconds' % (end - start))

        start = time.time()
        e_features.deep_run()
        end = time.time()
        logger.info('Deep-run processing time: %.4f seconds' % (end - start))

    logger.info('Extracted features:')
    features = e_features.get_features()
    for key, value in features.iteritems():
        logger.info('   %s: %f' % (key, value))

    logger.info('Finished')

if __name__ == '__main__':
    run()
