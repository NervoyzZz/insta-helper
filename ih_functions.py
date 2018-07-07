"""
Other functions that is make script functionality
"""

from InstagramAPI import InstagramAPI
import pickle
import os.path


def open_api(username, password):
    """
    open api. Load data from file if exists or create new file and data

    :param username: username
    :param password: password
    :return: data. dictionary {'api': api, 'follows': array}
             api is InstagramApi
             follows is array of users that you've already follows.
    """
    if os.path.exists(username.lower() + '.api'):
        f = open(username.lower() + '.api', 'br')
        data = pickle.load(f)
        f.close()
    else:
        api = InstagramAPI(username=username, password=password)
        follows = []
        api.login()
        data = {'api': api, 'follows': follows}
        f = open(username.lower() + '.api', 'bw')
        pickle.dump(data, f)
        f.close()
    return data


def unfollow_not_followers(api, delete=True):
    """
    Unfollow useras that don't follow you

    :param api: InstagramApi
    :return: not_follows: array of usernames that don't follow you
    """
    followers = api.getTotalSelfFollowers()
    followings = api.getTotalSelfFollowings()
    followers_name = []
    not_follows = []
    for i in range(len(followers)):
        followers_name.append(followers[i]['username'])
    for i in range(len(followings)):
        if followings[i]['username'] not in followers_name:
            not_follows.append(followings[i]['username'])
            if delete:
                api.unfollow(followings[i]['pk'])
    return not_follows
