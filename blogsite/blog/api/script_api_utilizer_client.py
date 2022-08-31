"""Creating a small script that utilize the Blog API"""
from pprint import pprint
import requests


SERVER = '127.0.0.1'
PORT = '8000'
BASE_URL = f'http://{SERVER}:{PORT}/api/'
URL_POSTS = f'{BASE_URL}list-create/'
URL_COMMENTS = f'{BASE_URL}comments/'
URL_TOKEN = f"{BASE_URL}token/"

token = ''
while True:
    user_name = input('Please enter your username: ')
    password = input('Please enter your password: ')
    token_payload = {
    "username": user_name,
    "password": password,
    }
    # Obtian key token for that given user
    token_data = requests.post(URL_TOKEN, data=token_payload)
    token_json = token_data.json()
    if token:= token_json.get('token'):
        break
    else:
        print('username or password is invalid')

headers = {
  'Authorization': f'Token {token}'
  }
payload = {'title': 'Hi Client',
        'body': 'Body Client',
        'status': 'published'
        }

# Create post
new_post = requests.post(URL_POSTS, headers=headers, data=payload)
pprint(new_post.json())

# Negative case: create post without authorization
post_without_authorization = requests.post(URL_POSTS, data=payload)
pprint(post_without_authorization.json())

# Get list of posts
list_posts = requests.get(URL_POSTS, headers=headers)
pprint(list_posts.json())

# Get list of comments
list_posts = requests.get(URL_COMMENTS, headers=headers)
pprint(list_posts.json())

if __name__ == '__main__':
  main()