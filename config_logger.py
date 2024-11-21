import logging
import sys

def create_logger(logger_name='lead_hunter'):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG) 
    fh = logging.FileHandler('lead_hunter.log', mode='w', encoding='utf-8')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    sys.stdout.reconfigure(encoding='utf-8')
    return logger
