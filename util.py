import hashlib
import json
from urllib.request import urlopen
from collections import namedtuple

def md5(value):
	return hashlib.md5(value.encode()).hexdigest()

def getJsonFromUrl(url):
	try:
		response = urlopen(url)
		str_response = response.read().decode('utf-8')
		return json.loads(str_response, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
	except:
		return None