# Import logic so that the inventoryapi module can be imported from up one directory without creating a package
from os import sys, path
sys.path.append(path.join(path.dirname(__file__), '..'))
from inventoryapi import InventoryAPI

import logging # for debug

# Init our Inventory API
inventoryApi = InventoryAPI(
	proxies = [ # Proxies in a list, includes protocol (socks5, http, etc) (default: None)
		'socks5://xxx:xxx@xxx.xxx.xxx.xxx:1234',
		'http://xxx:xxx@xxx.xxx.xxx.xxx:1234'
	],
	proxy_repeat = 1, # How many times we will reuse a proxy, meaning we will use a proxy 2 times if value is 1 (default: 1)
	timeout = 6, # How long until the request timeout is reached/no bytes received in seconds (default: 6)
)

logging.basicConfig(level=logging.DEBUG) # Allows us to see the debugging, here purely for the example, if a request fails it is logged as ERROR

inv = inventoryApi.get(
	steamid = '76561197993496553', # eg: '76561197993496553'
	appid = '753', # eg: '753'
	contextid = '6', # eg: '6'
	tradable = True, # Filters tradable items (default: True)
	retries = 5, # Max number of retries on current inventory request before throwing (default: 5)
	retry_delay = 1000, # The delay between retrys, not normal requests (default: 1000)
	language = 'english', # (default: english)
	count = 5000, # How many items to load per request, maximum is 5000 (default: 5000)
)

# Same as
inv = inventoryApi.get(
	'76561197993496553', # eg: '76561197993496553'
	'753', # eg: '753'
	'6', # eg: '6'
	True, # Filters tradable items (default: True)
)

# print(inv[0]) # first tradable item in the inventory (sorted by latest)
# print(inv[-1]) # last tradable item in the inventory (to last slot)
# print(len(inv)) # number of tradable items in the inventory
# print(inv)