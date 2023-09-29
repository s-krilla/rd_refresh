# rd_refresh

A set of useful scripts for managing a Real Debrid library

## Installation 

Install [rd_api_py](https://github.com/s-krilla/rd_api_py)

```
python -m pip install rd_api_py
```

Set environment variables in `.env`

```bash
RD_APITOKEN="your_token_here"
SLEEP=100 # Delay (ms) between requests - optional, default recommended
LONG_SLEEP=5000 # Long delay (ms) every 500 requests - optional, default recommended
```

## Docker
Use the following docker-compose.yml
```yaml
version: "3"

services:
  rd_refresh:
    container_name: rd_refresh
    build:
      context: .
      dockerfile: Dockerfile
    environment:
    - RD_APITOKEN=
    restart: unless-stopped
```
To run: `docker compose up -d --build`


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

