import random
import string
import json
import requests

# URL for Microsoft account creation
url = 'https://account.live.com/incentive/create'

# Headers for the request, change User-Agent to match actual browser UAs
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def create_account():
    # Microsoft might block some IPs, so use proxies
    proxy_list = ['http://178.62.28.189:8080', 'http://194.187.64.210:3128', 'http://45.76.139.126:3128']
    session = requests.Session()

    payload = {
        ' Marktplace ': 'XBOX',
        'IDない': generate_random_string(20),  # Fake Japanese ID, Microsoft seems to require this
        ' ua-country ': 'US'
    }

    try:
        resp = session.post(url, proxies=random.choice(proxy_list), headers=headers, json=payload)
        data = json.loads(resp.text)

        if data.get('action') == 'render':
            # Account creation successful, now we set the password
            payload = {'newPassword': generate_random_string(10), 'oldPassword': ''}
            session.post(url=data['action_url'], json=payload, headers=headers)
            print("Account created successfully!")
            return data['emailAddress']

        else:
            print("Error creating account, Microsoft says: ", data.get('message'))

    except requests.exceptions.RequestException as e:
        print("Request error:", e)

    return None

if __name__ == "__main__":
    for _ in range(5):  # Create 5 accounts for demonstration
        account = create_account()
        if account:
            print(f"Account details: {account}")
