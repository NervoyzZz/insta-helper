import os.path
import random

import ih_functions as ih

from InstagramAPI import InstagramAPI

username = input('Username [> ')
file_name = username.lower() + '.api'
if os.path.exists(file_name):
    data = ih.load_data(file_name)
else:
     password = input('Password [> ')
     data = ih.open_api(username, password)
estimation = ih.user_estimate(data['api'], data['api'].username_id)
print('Your estimation:', estimation)
not_follows = ih.unfollow_not_followers(data['api'])
print(not_follows)
estimation = ih.user_estimate(data['api'], data['api'].username_id)
print('Your estimation:', estimation)
