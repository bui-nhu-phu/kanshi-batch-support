__author__='buinhuphu'
__author_email__='bn.phu@afterfit.co.jp'

import logging
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from os import getenv

load_dotenv()
env = getenv('ENV', 'production')

FORMAT = f'%(asctime)s {env}.%(levelname)s: %(message)s'
LEVEL = logging.INFO

logging.Formatter.converter = lambda *args: datetime.now(tz=timezone(timedelta(hours=+9))).timetuple()
logger = logging.getLogger()
logger.setLevel(LEVEL)
if len(logger.handlers) > 0:
    logger.handlers[0].setFormatter(logging.Formatter(fmt=FORMAT))
else:
    logging.basicConfig(format=FORMAT)
