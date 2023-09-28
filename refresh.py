#!/usr/bin/env python3

import sys
import time
from functions import *

torrents = get_all('torrents')

if any(torrent['status'] == 'dead' for torrent in torrents):
    for torrent in torrents:
        if torrent['status'] == 'dead':
            logging.warning('Found dead torrents')
            refresh_torrent(torrent)
else:
    logging.info('Found no dead torrents')

logging.info('Done')

sys.exit()
