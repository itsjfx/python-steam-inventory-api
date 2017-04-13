# Steam Inventory API
# Written by jfx

# Python port of sebmorris/Oat's steam inventory api and port of DoctorMcKay's CEonItem
# sebmorris/Oat's steam-inventory-api: https://github.com/sebmorris/steam-inventory-api/blob/master/index.js
# DoctorMcKay's CEonItem: https://github.com/sebmorris/steam-inventory-api/blob/master/CEconItem.js
# :)

# TODO:
# * Proxies

import requests
import math
import time

inventory = []

class InventoryAPI:

	def merge_two_dicts(self, x, y):
		#https://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
		"""Given two dicts, merge them into a new dict as a shallow copy."""
		z = x.copy()
		z.update(y)
		return z
		
	def __init__(self, steamid, appid, contextid, tradeableOnly=True, proxy=""):
		self.steamid = steamid
		self.appid = appid
		self.contextid = contextid
		self.tradeableOnly = tradeableOnly
		
		if proxy: # currently not implemented yet
			self.proxy = proxy
	
	def makeRequest(self, lastAssetID=""):
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
		url = 'http://steamcommunity.com/inventory/'+self.steamid+'/'+self.appid+'/'+self.contextid+'?l=english&count=5000&start_assetid='+lastAssetID
		req = requests.get(url=url, headers=headers)
		return req.json() # use in-built requests module for json parsing
		
	def linkValues(self, asset, desc): # port of CEconItem.js from DoctorMcKay
		for descItem in desc:
			if descItem['classid'] == asset['classid'] and descItem['instanceid'] == asset['instanceid']:
				return self.merge_two_dicts(asset, descItem)
				break
	
	def execute(self, lastAssetID=""):
		# check to see if request went through
		done = False
		while not done:
			try:
				data = self.makeRequest(lastAssetID)
				done = True
			except:
				print "Error making request... trying again in 20 seconds."
				time.sleep(20)
		
		try: # we didn't get a proper response
			data['assets']
		except:
			raise ValueError('Malformed response')
		
		for item in data['assets']:
			generatedItem = self.linkValues(item, data['descriptions'])
			if self.tradeableOnly and generatedItem['tradable'] == 1:
				inventory.append(generatedItem)
			elif not self.tradeableOnly:
				inventory.append(generatedItem)
		return data
	
	def getItems(self):
		data = self.execute()
			
		if data['total_inventory_count'] > 5000 and data['last_assetid']: # if the inv is over 5000 items long then we need to send more requests with the last assetid
			for i in range(0, int(math.ceil(data['total_inventory_count'] / 5000))):
				try: # check if the request has the last_assetid, if it does keep going
					data['last_assetid'] = self.execute(data['last_assetid'])['last_assetid']
				except:
					pass
					break
		return inventory