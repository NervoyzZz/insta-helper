# ------------------------------------------------------------------------------
# Copyright © 2018 Daniil Nepryahin
# contacts: <nervoidaz@yandex.ru>
# License: https://opensource.org/licenses/MIT
# ------------------------------------------------------------------------------


"""
Other functions that is make script functionality
"""

from InstagramAPI import InstagramAPI

import os.path
import pickle
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
        # update not follow list
        follows = init_no_need_to_follow_list(data['api'])
        for f in follows:
            if f not in data['follows']:
                data['follows'].append(f)
        save_data(data['api'].username.lower() + '.api', data)
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
    :return: tuple of
        fraction of followings/followers
        number of followings
        number of followers
    """
    follower_count = len(api.getTotalFollowers(user_id))
    followings_count = len(api.getTotalFollowings(user_id))
    return followings_count / follower_count, followings_count, follower_count


def give_likes_to_user(api, user_id, likes_count=10, sleep_time=1):
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
    likes = likes_count if feed_len > likes_count else (feed_len // 2)
    for i in range(likes):
        # get random media
        media_id = random.choice(feed)['id']
        # and like it
        api.like(media_id)
        # wait some_time
        time.sleep(sleep_time)


def user_like_follow(data, user_id, likes_count=10,
                     thresholds=(0.7, 1.2), sleep_time=1):
    """
    Function that estimate user and then decide to like him and follow

    :param :data: data dictionary with 'api' and 'follows' keys
    :param :user_id: user id that you want to like/follow
    :param :likes_count: how much likes give to user
    :param :sleep_time: dellay between likes
    :param :thresholds: min border and max border to likes
                        if estimation less then min => user will not
                        follow you back
                        if estimation greater then max => user can follow
                        you without your following (or he can be not true
                        user)
    :return: bool True if follows user and False if not follows
    """
    api = data['api']
    follows = data['follows']
    # check user
    # if he in our 'black' list
    if user_id in follows:
        return False
    # estimate him
    estimate = user_estimate(api, user_id)[0]
    # give him likes anyway
    give_likes_to_user(api, user_id, likes_count, sleep_time)
    # decide to follow him
    if estimate < thresholds[0] or estimate > thresholds[1]:
        return False
    else:
        api.follow(user_id)
        follows.append(user_id)
        data['follows'] = follows
        return True


def user_followers_like_follow_helper(data, user_id, users_count=25,
                                      likes_count=10,
                                      thresholds=(0.7, 1.2),
                                      sleep_time=1):
    """
    Helper function. It gets user followers list. Then choice
    some users and like and follow them.

    :param :data: data dictionary with 'api' and 'follows' keys
    :param :user_id: user id. His followers function will like and follow
    :param :user_count: how much users function should like/follow
    :param :likes_count: how much gives likes
    :param :sleep_time: dellay between likes
    :param :thresholds: min border and max border to likes
                        if estimation less then min => user will not
                        follow you back
                        if estimation greater then max => user can follow
                        you without your following (or he can be not true
                        user)
    :return: dictionary {'user_name': staus} where status ia True or False
             follow this user or not
    """
    result = {}
    api = data['api']
    # get user followers
    followers = api.getTotalFollowers(user_id)
    # choose some users
    users_count = users_count if users_count < len(followers) else (
        len(followers) // 2)
    for i in range(users_count):
        user = random.choice(followers)
        try:
            status = user_like_follow(data, user['pk'], likes_count,
                                      thresholds, sleep_time)
            result[user['username']] = status
        except:
            print('ERROR')
    # save data
    save_data(api.username.lower() + '.api', data)    
    return result


def results_log(results, to_file=False, file_name=''):
    """
    Function to write log information.

    :param results: data to show.
    :param to_file: flag to write log to file or to the screen.
    :param file_name: log file name.
    :return: None
    """
    if not to_file:
        print(results)
    else:
        if os.path.exists(file_name):
            f = open(file_name, 'a')
        else:
            f = open(file_name, 'w')
        f.write(results)
        f.write('\n')
        f.close()
