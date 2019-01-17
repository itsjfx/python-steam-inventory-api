# Steam Inventory API
# Written by jfx
# https://jfx.ac
# https://github.com/itsjfx/python-steam-inventory-api/

import requests, logging
from time import sleep

class InventoryAPIException(Exception):
    pass
	
class InventoryAPI:
	def merge_two_dicts(self, x, y):
		z = x.copy()
		z.update(y)
		return z
		
	def proxy(self):
		if not self.proxies:
			return None
	
		if (self.currProxyRepeat < self.proxyRepeat): # We can keep using this one
			self.currProxyRepeat = self.currProxyRepeat + 1
		else: # Cycle through the proxies
			self.currProxyRepeat = 0
			if (self.proxyPos == len(self.proxies) - 1):
				self.proxyPos = 0
			else:
				self.proxyPos = self.proxyPos + 1
			
		return self.proxies[self.proxyPos]
		
	def __init__(self, proxies=None, proxyRepeat=1, timeout=6):
		self.inventory = []
		self.proxies = proxies
		self.proxyPos = 0
		self.currProxyRepeat = -1 # -1 or breaks on initial proxy
		self.proxyRepeat = proxyRepeat
		self.timeout = timeout
		self.logger = logging.getLogger(__name__)
	
	def makeRequest(self, options, last_assetid=""):
		headers = {
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
			"referer": "https://steamcommunity.com/profiles/{}/inventory".format(options['steamid'])
		}
		url = 'https://steamcommunity.com/inventory/{}/{}/{}?l={}&count={}&start_assetid={}'.format(options['steamid'], options['appid'], options['contextid'], options['language'], options['count'], last_assetid)
		
		proxy = self.proxy()
		proxies = {
		  'http': proxy,
		  'https': proxy
		}
		
		self.logger.debug("Requesting. Start {}, Proxy {}, Retries {}, Items {}".format(last_assetid, proxies, options['retries'], len(self.inventory)))
		
		try:
			req = requests.get(url=url, headers=headers, proxies=proxies, timeout=self.timeout)
			return req.json()
		except Exception as e:
			self.logger.error("Error making request: {}".format(e))
			if options['retries'] > 0:
				self.logger.debug("Retrying in {} seconds".format(options['retryDelay']))
				sleep(options['retryDelay'])
				options['retries'] = options['retries'] - 1
				if self.proxies:
					self.logger.debug("Force cycling proxy")
					self.currProxyRepeat = self.proxyRepeat # Force the proxies to rotate so we don't repeat the same one on our retry, as it may be temporarily available
				return self.makeRequest(options, last_assetid)
			else:
				raise InventoryAPIException("Out of retries")
		
	def linkValues(self, asset, desc):
		for descItem in desc:
			if descItem['classid'] == asset['classid'] and descItem['instanceid'] == asset['instanceid']:
				return self.merge_two_dicts(asset, descItem)
				
	def execute(self, options, last_assetid=None):
		data = self.makeRequest(options, last_assetid)
		
		if not 'assets' in data: # we didn't get a proper response, this may happen if Steam blocks the proxy!!
			raise InventoryAPIException('Malformed response')
		
		for item in data['assets']:
			generatedItem = self.linkValues(item, data['descriptions'])
			
			# Make them True or False instead of 0 or 1
			generatedItem['currency'] = not not generatedItem['currency']
			generatedItem['tradable'] = not not generatedItem['tradable']
			generatedItem['marketable'] = not not generatedItem['marketable']
			generatedItem['commodity'] = not not generatedItem['commodity']
			
			if (options['tradable'] and generatedItem['tradable']) or not options['tradable']:
				self.inventory.append(generatedItem)
		
		if 'more_items' in data:
			return self.execute(options, data['last_assetid'])
		else:
			return self.inventory
	
	def get(self, steamid, appid, contextid, tradable=True, retries=5, retryDelay=1000, language='english', count=5000):	
		self.inventory = []
		
		options = {
			"steamid": steamid,
			"appid": appid,
			"contextid": contextid,
			"count": count,
			"language": language,
			"tradable": tradable,
			"retries": retries,
			"retryDelay": retryDelay/1000.0
		}
		
		return self.execute(options, None)