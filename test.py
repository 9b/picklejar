import requests
from picklejar import brine

@brine()
def hello():
	lala = requests.get('https://www.google.com')

hello()	
