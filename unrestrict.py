#!/usr/bin/env python3

import sys
from functions import *

torrents = get_all('torrents')
downloads = get_all('downloads')

torrent_links = find_torrent_links(torrents)
download_links = find_download_links(downloads)
restricted_links = find_restricted_links(torrent_links, download_links)

logging.debug(restricted_links)

bad_links = []

for link in restricted_links:
    response = RD().unrestrict.link(link).json()
    if 'error_code' in response:
        if response['error_code'] == 19:
            bad_links.append(link)
            logging.warning('Found bad link:' + '\n' + str(link))
    else:
        logging.info('Unrestricted:' + '\n' + response['filename'])

if len(bad_links) > 0:
    logging.warning('Found bad links:' + '\n' + str(bad_links))

bad_torrents = find_bad_torrents(torrents, bad_links)

for bad_torrent in bad_torrents:
    refresh_torrent(bad_torrent)

logging.info('Done')    

sys.exit()