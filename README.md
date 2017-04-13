# python-steam-inventory-api
Steam Inventory API written in Python for the new endpoints

## Main features
- Python implementation of Doctor McKay's CEonItem.js
- Python implementation of requesting inventory data and returning it
- In-built filter for tradeable or non-tradeable items

## TO-DO
- Proxies

## Requirements
See requirements.txt
 

## Examples
```
from inventoryapi import InventoryAPI

inv = InventoryAPI(steamid='76561197993496553',appid='730',contextid='2',tradeableOnly=True).getItems()

print inv[0] # first tradeable item in the inventory (sorted by latest)
print inv[-1] # last tradeable item in the inventory (to last slot)
print len(inv) # number of tradeable items in the inventory
```
