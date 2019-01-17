# python-steam-inventory-api
Steam Inventory API written in Python for the new endpoints

## Main features
- Python implementation of getting steam inventory for any game/contextid, with matching descriptions
- Python 2 & 3 supported!!
- In-built filter for tradable or non-tradable items
- Proxy support, supports a list of socks/http/etc proxies, automatically cycles them with customisable values (how many repeats for same proxy)
- Retries and customisable values for retry (retry delay, number of retries)
- Optional debug logging

## Mentions
- Oat/sebmorris and Doctor McKay for their inventory api's which inspired me to write my own and base mine off, especially Seb's

## Requirements
See requirements.txt

## Proxy info
Needs requests[socks] which will install pysocks to allow proxies to work for socks proxies

For proxies it uses anything python requests supports under its proxies param, socks5 and http have been tested to work

## Examples
See examples/example.py