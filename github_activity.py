import sys
import requests
from datetime import datetime

def get_user_activity(username: str): 
    url = f'https://api.github.com/users/{username}/events'
    response = requests.get(url)
    if response.status_code == 200:
        events = response.json()
        for event in events:
            repo = event['repo']['name']
            payload = event['payload']
            date = event['created_at']
            
            match event['type']:
                case 'CreateEvent':
                    print(f'{format_date(date)} ~ Created {payload['ref_type']} {payload['ref']}')
                case 'PushEvent':
                    print(f'{format_date(date)} ~ Pushed {payload['size']} commit(s) to {repo}')
    elif response.status_code == 404:
        print("(T-T) User not found.")
    else:
        print(f'HTTP Error: {response.status_code}')

def format_date(date: str) -> str:
    dt = datetime.fromisoformat(date.replace("Z",  "+00:00"))
    return dt.strftime("%d.%m.%y")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        get_user_activity(sys.argv[1])
    else:
        print("Please enter a GitHub username without spaces as an argument")
