"""
Other functions that is make script functionality
"""

from InstagramAPI import InstagramAPI
import pickle
import os.path
import random
import time


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
        api.login()        
        follows = init_no_need_to_follow_list(api)
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


def init_no_need_to_follow_list(api):
    """
    create list for data dictionary where users that
    there's no need to follow in it.

    :param api: api param from data dictionary
    :return: list with no need to follow users
    """
    follows = []
    # no need to follow user that you've alredy followed
    # or that follows you
    self_followers = api.getTotalSelfFollowers()
    self_followings = api.getTotalSelfFollowings()
    for i in range(len(self_followers)):
        follows.append(self_followers[i]['pk'])
    for i in range(len(self_followings)):
        s_f = self_followings[i]['pk']
        if s_f not in follows:
            follows.append(self_followings[i]['pk'])
    return follows


def user_estimate(api, user_id):
    """
    Estimation of user. Should we follow him?

    :param :api: api param from data dictionary
    :param :user_id: id of user whom we want to estimate
    :return: fraction of followings/followers. Just a float number
    """
    follower_count = len(api.getTotalFollowers(user_id))
    followings_count = len(api.getTotalFollowings(user_id))
    return followings_count / follower_count


def give_likes_to_user(api, user_id, likes_count=5, sleep_time=0.5):
    """
    That function gives likes to random media for user

    :param :api: api param from data dictionary
    :param :user_id: user id Whom likes should be gived
    :param :likes_count: how much likes give to user
    :param :sleep_time: dellay between likes
    :return: None
    """
    # get user feed
    feed = api.getTotalUserFeed(user_id)
    feed_len = len(feed)
    likes = likes_count if feed_len > likes_count else (feed_len
                                                        / (likes_count
                                                           + 1))
    for i in range(likes):
        # get random media
        media_id = random.choice(feed)['id']
        # and like it
        api.like(media_id)
        # wait some_time
        time.sleep(sleep_time)
    
        
        
    
    

