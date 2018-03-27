# -*- coding: utf-8 -*

# Steam Inventory API
# Written by jfx
# https://github.com/itsjfx/

# Python port of a steam inventory api, inspired by many projects - mainly Oat's nodejs inventory api and Doctor McKay's
# Made in Python 2.7 but should probably work in later versions if you fix some syntax, one day I'll move on to 3...
# Code might need a re-write/look at for improvements since it's old, but it does the job.

import requests, math, time

inventory = []

class InventoryAPI:

	def merge_two_dicts(self, x, y):
		#https://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
		#Given two dicts, merge them into a new dict as a shallow copy.
		z = x.copy()
		z.update(y)
		return z
		
	def __init__(self, steamid, appid, contextid, tradeableOnly=True, proxy=None):
		self.steamid = steamid
		self.appid = appid
		self.contextid = contextid
		self.tradeableOnly = tradeableOnly
		self.proxy = proxy
	
	def makeRequest(self, lastAssetID=""):
		headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"} # not sure if required but might as well
		url = 'http://steamcommunity.com/inventory/{}/{}/{}?l=english&count=5000&start_assetid={}'.format(self.steamid, self.appid, self.contextid, lastAssetID)
		# build the proxy, luckily putting None will make it not use a proxy as well
		proxies = {
		  'http': self.proxy,
		  'https': self.proxy
		}
		req = requests.get(url=url, headers=headers, proxies=proxies)
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
			except Exception as e:
				print "Error making request: {} ... trying again in 20 seconds.".format(e)
				time.sleep(20)
		
		try: # we didn't get a proper response, this may happen if Steam blocks the proxy!!
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
