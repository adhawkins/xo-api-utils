import requests

class xoAPI:
	API_BASE="/rest/v0/"

	def __init__(self, URL, token):
		self.URL = URL
		self.token = token

	def makeRequest(self, object):
		cookies = {
			"authenticationToken": self.token
		}

		if object.startswith(xoAPI.API_BASE):
			url = f"{self.URL}{object}"
		else:
			url = f"{self.URL}{xoAPI.API_BASE}{object}"

		ret = requests.get(url, cookies = cookies)
		ret.raise_for_status()
		return ret.json()

