#!/usr/bin/env python3

import sys
import os
import logging

from dotenv import load_dotenv
load_dotenv()

from rdapi import RD
RD = RD()

LOGLEVEL = os.getenv('LOGLEVEL', 'INFO').upper()
logging.basicConfig(
    level=LOGLEVEL,
    format='%(asctime)s:%(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler('rd_refresh.log'),
        logging.StreamHandler(sys.stdout)
    ]
    )

def get_all(type):
    page = 1
    processed = 0
    collected = []
    while True:
        request = None
        if type == 'torrents':
            request = RD.torrents.get(limit=2500, page=page)
        else:
            request = RD.downloads.get(limit=2500, page=page)
        data = request.json()
        collected += data
        total = int(request.headers['X-Total-Count'])
        processed = processed + len(data)
        remaining = total - processed
        page = page + 1

        if remaining == 0:
            break
    logging.info('Retrieved %s %s from RD', str(len(collected)), type)
    return collected

def refresh_torrent(torrent):
    old_torrent = RD.torrents.info(torrent['id']).json()
    logging.warning('Refreshing old torrent:\n%s', str(old_torrent['filename']))
    old_torrent_files = old_torrent['files']
    files_to_keep = []
    for file in old_torrent_files:
        if file['selected'] == 1:
            files_to_keep.append(file['id'])
    cs_files_to_keep = ','.join(map(str, files_to_keep))
    logging.info('Files to keep:\n%s', cs_files_to_keep)
    new_torrent = RD.torrents.add_magnet(old_torrent['hash']).json()
    logging.info('New magnet added')
    RD.torrents.select_files(new_torrent['id'], cs_files_to_keep)
    logging.info('New files selected')
    RD.torrents.delete(old_torrent['id'])
    logging.info('Old torrent deleted')
    return  

def find_torrent_links(torrents):
    torrent_links = []
    for torrent in torrents:
        if torrent['status'] == 'downloaded':
            if torrent['links'] != []:
                for link in torrent['links']:
                    torrent_links.append(link)
    logging.info('Found %s torrent link(s)', str(len(torrent_links)))
    return torrent_links

def find_download_links(downloads):
    download_links = []
    for download in downloads:
        download_links.append(download['link'])
    logging.info('Found %s download link(s)', str(len(download_links)))
    return download_links

def find_restricted_links(torrent_links, download_links):
    restricted_links = list(set(torrent_links).difference(download_links))
    logging.info('Found %s restricted link(s)', str(len(restricted_links)))
    return restricted_links

def find_bad_torrents(torrents, bad_links):
    bad_torrents = []
    for link in bad_links:
        bad_torrents.append(find(torrents, link))
    dedupe = []
    for bad_torrent in bad_torrents:
        if bad_torrent not in dedupe:
            dedupe.append(bad_torrent)
    bad_torrents = dedupe
    logging.warning('%s bad torrent(s)', str(len(bad_torrents)))
    return bad_torrents
    
def find(torrents, link):
    for torrent in torrents:
        if link in torrent["links"]:
            return torrent