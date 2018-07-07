# !usr/bin/python3

"""
script that can do something boring routine in Instagram such as
unfollow not following you users
like other photos
follow other users
"""

import ih_functions as ih

username = input("Username [> ")
password = input("Password [> ")

data = ih.open_api(username, password)
api = data['api']
follows = data['follows']
not_follows = ih.unfollow_not_followers(api)
print(not_follows)
