#!/usr/bin/env python3

import sys
from functions import *

torrents = get_all('torrents')

for torrent in torrents:
    if torrent['status'] == 'dead':
        print('Found dead torrent')
        refresh_torrent(torrent)

print('Finished')

sys.exit()
