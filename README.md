# rd_refresh

A set of useful scripts for managing a Real Debrid library

## Installation 

Install [rd_api_py](https://github.com/s-krilla/rd_api_py)

```
pip install rd_api_py
```

Set environment variables in `.env`

```bash
RD_APITOKEN="your_token_here"
REFRESH_INTERVAL=15 # Interval (minutes) between refreshes - optional
LOGLEVEL=INFO # Default INFO - optional

# rd_api_py configuration - optional, defaults recommended 
SLEEP=2000 # Delay (ms) between requests
LONG_SLEEP=30000 # Long delay (ms) every 500 requests
```

## Usage

Set up cron jobs to execute operations - for example:
```bash
sudo chmod +x refresh.py
```

```
*/15 * * * * /path/to/refresh.py
```

Or use Docker. 

## Docker

```yaml
version: "3"

services:
  rd_refresh:
    container_name: rd_refresh
    build:
      context: .
      dockerfile: Dockerfile
    env_file:
      - .env                         # Be sure to change the env file to `.env` and update API Token.
    environment:
      - RD_APITOKEN=yourtokenhere    # Alternatively set the token here instead of .env file. 
    restart: unless-stopped
```
To run: `docker compose up -d --build`

### refresh.py

- Finds "dead" torrents
- Re-adds torrents
- Selects the same files
- Deletes the old torrent

### unrestrict.py 

**Warning - excessive API calls**

- Compares torrent and downloads and finds restricted downloads links
- Unrestricts download links
- Refreshes "bad" torrents

