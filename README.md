# python-steam-inventory-api
Steam Inventory API written in Python for the new endpoints

## Main features
- Python implementation of requesting inventory data and returning it
- In-built filter for tradeable or non-tradeable items
- Proxy support!

## To-do
- Get tags

## Mentions
- Oat/sebmorris and Doctor McKay for their inventory api's which inspired me to write my own and base mine off

## Requirements
See requirements.txt

## Proxy info
Needs requests[socks] which will install pysocks to allow proxies to work

For proxies it uses anything python requests supports under its proxies dictionary, using the proxy the user inputs as a http and https proxy  
I have only used and tested socks5 proxies - to use one do proxy="socks5://xxx.xxx.xxx.xxx:12345"

## Examples
See examples/example.py
