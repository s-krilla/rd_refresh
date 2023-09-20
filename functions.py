#!/usr/bin/env python3

from rdapi import RD

def get_all(type):
    page = 1
    processed = 0
    collected = []
    while True:
        request = None
        if type == 'torrents':
            request = RD().torrents.get(limit=2500, page=page)
        else:
            request = RD().downloads.get(limit=2500, page=page)
        data = request.json()
        collected += data
        total = int(request.headers['X-Total-Count'])
        processed = processed + len(data)
        remaining = total - processed
        page = page + 1

        if remaining == 0:
            break
    print('Retrieved ' + str(len(collected)) + ' ' + type + ' from RD')            
    return collected

def refresh_torrent(torrent):
    old_torrent = RD().torrents.info(torrent['id']).json()
    print('Old torrent: ' + str(old_torrent['filename']))
    old_torrent_files = old_torrent['files']
    files_to_keep = []
    for file in old_torrent_files:
        if file['selected'] == 1:
            files_to_keep.append(file['id'])
    cs_files_to_keep = ','.join(map(str, files_to_keep))
    print('Files to keep: ' + cs_files_to_keep)
    new_torrent = RD().torrents.add_magnet(old_torrent['hash']).json()
    print('New magnet added')
    RD().torrents.select_files(new_torrent['id'], cs_files_to_keep)
    print('New files selected')
    RD().torrents.delete(old_torrent['id'])
    print('Old torrent deleted')
    return  

def find_torrent_links(torrents):
    torrent_links = []
    for torrent in torrents:
        if torrent['status'] == 'downloaded':
            if torrent['links'] != []:
                for link in torrent['links']:
                    torrent_links.append(link)
    print('Found ' + str(len(torrent_links)) + ' torrent link(s)')
    return torrent_links

def find_download_links(downloads):
    download_links = []
    for download in downloads:
        download_links.append(download['link'])
    print('Found ' + str(len(download_links)) + ' download link(s)')
    return download_links

def find_restricted_links(torrent_links, download_links):
    restricted_links = list(set(torrent_links).difference(download_links))
    print('Found ' + str(len(restricted_links)) + ' restricted link(s)')
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
    print(str(len(bad_torrents)) + ' bad torrent(s)')
    return bad_torrents
    
def find(torrents, link):
    for torrent in torrents:
        if link in torrent["links"]:
            return torrent