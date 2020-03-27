# Horse racing crawler

Crawling horse racing information from "Korea Horse Association" website.

Data is saved on `data` folder, with filename `[year].tsv`.
File encoding type is `utf-8`, delimiter is `\t` and it has header.

When crawling failed, then error logs are written on `error.log` file.

## How to use

```bash
# Install required package
$ pip install -r requirements.txt
# Crawling 2015-01-01 ~ 2019-12-31 information with pool size 5.
$ python main.py --start-year 2015 --end-year 2019 --pool-size 5
```

## Argument description

- --start-year / -s
  * Set start year with YYYY format.
  * required
- --end-year / -e
  * Set end year with YYYY format.
  * required
- --pool-size / -p
  * Set thread pool size.
  * default 4

## Requirements

- beautifulsoup4
- requests
