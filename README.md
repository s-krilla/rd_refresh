# rd_refresh

A set of useful scripts for managing a Real Debrid library

## Installation 

Copy `rd_api_py` into the `rd_refresh` directory

## Usage

Set up cron jobs to execute operations - for example:
```
sudo chmod +x unrestrict.py
sudo chmod +x refresh.py
```

```
0 3 * * * /some/path/unrestrict.py
*/15 * * * * /some/path/refresh.py
```

### unrestrict.py

- Compares torrent and downloads and finds restricted downloads links
- Unrestricts download links
- Refreshes bad torrents

### refresh.py

- Finds "dead" torrents
- Re-adds torrents
- Selects the same files
- Deletes the old torrent

