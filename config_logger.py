import logging

def create_logger():
    logger = logging.getLogger('lead_hunter')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('lead_hunter.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
