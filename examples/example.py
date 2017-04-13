from inventoryapi import InventoryAPI

inv = InventoryAPI(steamid='76561197993496553',appid='730',contextid='2',tradeableOnly=True).getItems()
# inv = InventoryAPI('76561197993496553','730','2',True).getItems() # both are the same thing

print inv[0] # first tradeable item in the inventory (sorted by latest)
print inv[-1] # last tradeable item in the inventory (to last slot)
print len(inv) # number of tradeable items in the inventory