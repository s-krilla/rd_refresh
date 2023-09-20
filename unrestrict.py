#!/usr/bin/env python3

import sys
from functions import *

torrents = get_all('torrents')
downloads = get_all('downloads')

torrent_links = find_torrent_links(torrents)
download_links = find_download_links(downloads)
restricted_links = find_restricted_links(torrent_links, download_links)

print(restricted_links)

bad_links = []

for link in restricted_links:
    response = RD().unrestrict.link(link).json()
    print(response)
    # data = response.json()
    if 'error_code' in response:
        if response['error_code'] == 19:
            bad_links.append(link)

print('bad link ' + str(bad_links))

bad_torrents = find_bad_torrents(torrents, bad_links)

for bad_torrent in bad_torrents:
    refresh_torrent(bad_torrent)

sys.exit()