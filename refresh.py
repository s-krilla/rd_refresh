#!/usr/bin/env python3

import sys
import os
import time
from functions import *

from dotenv import load_dotenv
load_dotenv()

interval = int(os.getenv('REFRESH_INTERVAL', 15)) * 60 

while True:

    torrents = get_all('torrents')

    if any(torrent['status'] == 'dead' for torrent in torrents):
        for torrent in torrents:
            if torrent['status'] == 'dead':
                logging.warning('Found dead torrents')
                refresh_torrent(torrent)
    else:
        logging.info('Found no dead torrents')

    logging.info('Done')

    logging.info('Sleeping %s minutes', int(interval / 60))

    time.sleep(interval)
