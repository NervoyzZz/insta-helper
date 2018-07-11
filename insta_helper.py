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
import random


username = input("Username [> ")
file_name = username.lower() + '.api'

if os.path.exists(file_name):
    data = ih.load_data(file_name)
else:
    password = input("Password [> ")
    data = ih.open_api(username, password)

# ~~~~~~~~~~~~~~~~~~~~~~~
# Unfollow not followers

# not_follows = ih.unfollow_not_followers(data['api'])
# print(not_follows)

# ~~~~~~~~~~~~~~~~~~~~~~~
# Your estimation

# estimation = ih.user_estimate(data['api'], data['api'].username_id)
# print(estimation)

# ~~~~~~~~~~~~~~~~~~~~~~~
# Follow and like new users

followings = data['api'].getTotalSelfFollowings()
user = random.choice(followings)
print(user['username'])
res = ih.user_followers_like_follow_helper(data, user['pk'], 15, 10, 1,
                                           (0.6, 1.1))
print(res)

# ~~~~~~~~~~~~~~~~~~~~~~~~
# Update not follow again list

#follows = ih.init_no_need_to_follow_list(data['api'])
#for f in follows:
#    if f not in data['follows']:
#        data['follows'].append(f)
#ih.save_data(data['api'].username.lower() + '.api', data)
