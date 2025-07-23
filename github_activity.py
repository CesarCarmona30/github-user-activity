import sys
import requests

username = sys.argv[1]
url = f'https://api.github.com/users/{username}/events'
print(requests.get(url).json())
print(requests.get(url).status_code)
