# !usr/bin/python3

"""
script that can do something boring routine in Instagram such as
unfollow not following you users
like other photos
follow other users
"""

import argparse
import ih_functions as ih
from InstagramAPI import InstagramAPI
import os.path
import random


def main(args):
    """
    Main function of script

    :param :args: args from command line
    :return: None
    """
    username = args.username if args.username != '' else input(
        'Username [> ')
    file_name = username.lower() + '.api'
    if os.path.exists(file_name):
        data = ih.load_data(file_name)
    else:
         password = args.password if args.password != '' else input(
             'Password [> ')
         data = ih.open_api(username, password)
    if args.unfollow == 1:
        not_follows = ih.unfollow_not_followers(data['api'])
        print(not_follows)
    if args.estimate == 1:
        estimation = ih.user_estimate(data['api'], data['api'].username_id)
        print('Your estimation:', estimation)
    print('It\'s like/follow time!')
    followings = data['api'].getTotalSelfFollowings()
    user = random.choice(followings)
    print(user['username'])
    res = ih.user_followers_like_follow_helper(data, user['pk'],
                                               25, 10, 1, (0.7, 1.2))
    print(res)
            


if __name__ == '__main__':
    # use parser to get parameters from command line
    parser = argparse.ArgumentParser(
        description='Helper for instagram. Can unfolow not folowers,'
                    'like and follow new users that can help you with'
                    'profile boosting.')
    parser.add_argument('--username', help='your username', default='')
    parser.add_argument('--password', help='your password', default='')
    parser.add_argument('--unfollow', help='0 to not unfollow and 1 to'
                        'unfollow not followers', type=int, default=0)
    parser.add_argument('--estimate', help='0 or 1. Estimation of your'
                        'profile (fraction followings/followers)',
                        type=int, default=0)
    args = parser.parse_args()
    main(args)
