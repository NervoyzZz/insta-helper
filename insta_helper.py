# !usr/bin/python3

"""
script that can do something boring routine in Instagram such as
unfollow not following you users
like other photos
follow other users
"""

import ih_functions as ih
from InstagramAPI import InstagramAPI
import os.path


username = input("Username [> ")
file_name = username.lower() + '.api'

if os.path.exists(file_name):
    data = ih.load_data(file_name)
else:
    password = input("Password [> ")
    data = ih.open_api(username, password)

# not_follows = ih.unfollow_not_followers(data['api'])
# print(not_follows)
# estimation = ih.user_estimate(data['api'], data['api'].username_id)
# print(estimation)

