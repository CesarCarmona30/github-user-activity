import sys
import requests
from datetime import datetime

def fetch_events(username): 
    url = f'https://api.github.com/users/{username}/events'
    response = requests.get(url)

    if response.status_code == 404:
        raise ValueError("User not found")
    
    return response.json()

def format_date(iso):
    dt = datetime.fromisoformat(iso.replace("Z",  "+00:00"))
    return dt.strftime("%d.%m.%y")

def print_events(events):
    for event in events:
        repo = event['repo']['name']
        payload = event['payload']
        date = event['created_at']
        evt = event['type']

        match evt:
            case 'CreateEvent':
                print(f' {format_date(date)} ~ Created {payload['ref_type']} in {repo}')
            case 'PushEvent':
                print(f' {format_date(date)} ~ Pushed {payload['size']} commit(s) to {repo}')
            case 'WatchEvent':
                print(f' {format_date(date)} ~ Starred {repo}')
            case 'ForkEvent':
                print(f' {format_date(date)} ~ Forked {repo}')
            case 'PullRequestEvent':
                print(f' {format_date(date)} ~ {payload['action'].capitalize()} a pull request in {repo}')
            case 'IssuesEvent':
                print(f' {format_date(date)} ~ {payload['action'].capitalize()} an issue in {repo}')
            case 'DeleteEvent':
                print(f' {format_date(date)} ~ Deleted {payload['ref_type'].capitalize()} in {repo}')
            case _:
                print(f' {format_date(date)} ~ {evt.replace("Event", "")} in {repo}')

def main(username):
    try:
        events = fetch_events(username)
        if not events:
            print(f'No recent activity for {username}')
            return
        print(f'Activity of {username}')
        print_events(events)
    except ValueError as err:
        print(f'(T-T) {err}.')
    except requests.HTTPError as err:
        print(f'HTTP Error: {err.response.status_code}')
    except requests.RequestException:
        print(f'Network Error: Please check your connection.')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please enter a GitHub username as an argument: `python github_activity <username>`")
        sys.exit(1)
    main(sys.argv[1])
