"""
Other functions that is make script functionality
"""

from InstagramAPI import InstagramAPI
import pickle
import os.path


def load_data(file_name):
    """
    load data from file

    :param file_name: file name
    :return: data: dictionary with 'api' and 'follows' keys
    """
    data = None
    if os.path.exists(file_name):
        f = open(file_name, 'br')
        data = pickle.load(f)
        f.close()
    return data


def save_data(file_name, data):
    """
    save data to file

    :param file_name: file name
    :param data: data to save
    :return: None
    """
    f = open(file_name, 'bw')
    pickle.dump(data, f)
    f.close()


def open_api(username, password):
    """
    open api. Load data from file if exists or create new file and data

    :param username: username
    :param password: password
    :return: data. dictionary {'api': api, 'follows': array}
             api is InstagramApi
             follows is array of users that you've already follows.
    """
    file_name = username.lower() + '.api'
    if os.path.exists(file_name):
        data = load_data(file_name)
    else:
        api = InstagramAPI(username=username, password=password)
        follows = []
        api.login()
        data = {'api': api, 'follows': follows}
        save_data(file_name, data)
    return data


def unfollow_not_followers(api, delete=True):
    """
    Unfollow useras that don't follow you

    :param api: InstagramApi
    :param delete: flag to delete or not unfollowers
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
