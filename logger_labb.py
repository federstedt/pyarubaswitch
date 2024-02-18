from pyarubaswitch.logger import get_logger

logger = get_logger(log_level='DEBUG')

logger.debug('debug logg')
logger.info('info logg')
logger.warning('warning logg')
print(logger.name)
print(logger.level)
