import logging
from pathlib import Path
import os, errno, time

def logging_init():
    log_bool = True
    curr_path = os.path.dirname(os.path.realpath(__file__))
    logging_path = Path(curr_path + "/logs")

    try:
        os.makedirs(logging_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='/%m/%d/%Y %I:%M:%S %p',
                            filename=os.path.join(
                                logging_path,
                                time.strftime("%Y-%m-%d") + '.log'),
                            level=logging.DEBUG)
