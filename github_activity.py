import sys
import requests

def get_activity(username): 
    url = f'https://api.github.com/users/{username}/events'
    response = requests.get(url)
    if response.status_code == 200:
        return response

if __name__ == "__main__":
    if len(sys.argv) == 1:
        get_activity(sys.argv[1])
    else:
        print("Please enter a GitHub username without spaces as an argument")
