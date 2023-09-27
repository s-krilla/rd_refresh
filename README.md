# rd_refresh

A set of useful scripts for managing a Real Debrid library

## Installation 

Install [rd_api_py](https://github.com/s-krilla/rd_api_py)

```
python -m pip install rd_api_py
```

Set `RD_APITOKEN` in `.env`

## Usage

Set up cron jobs to execute operations - for example:
```bash
sudo chmod +x unrestrict.py
sudo chmod +x refresh.py
```

```
0 3 * * * /path/to/unrestrict.py
*/15 * * * * /path/to/refresh.py
```

### unrestrict.py

- Compares torrent and downloads and finds restricted downloads links
- Unrestricts download links
- Refreshes "bad" torrents

### refresh.py

- Finds "dead" torrents
- Re-adds torrents
- Selects the same files
- Deletes the old torrent

