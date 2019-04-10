# !usr/bin/python3


# ------------------------------------------------------------------------------
# Copyright © 2018 Daniil Nepryahin
# contacts: <nervoidaz@yandex.ru>
# License: https://opensource.org/licenses/MIT
# ------------------------------------------------------------------------------


"""
script that can do something boring routine in Instagram such as
unfollow not following you users
like other photos
follow other users
"""

import argparse
import datetime
import os.path
import random
import time

import ih_functions as ih


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
    should_work = True
    while should_work or args.work_on_loop:
        now = datetime.datetime.now()
        is_work_time = (now.time().hour == args.start_hour and
                        now.time().minute == args.start_min or
                        not args.work_on_loop)
        if should_work and is_work_time:
            if args.unfollow:
                not_follows = ih.unfollow_not_followers(data['api'])
                ih.results_log(str(not_follows), args.work_on_loop, args.log_file)
            if args.estimate:
                estimation = ih.user_estimate(data['api'], data['api'].username_id)
                ih.results_log('Estimation: {1}/{2} = {0}'.format(estimation[0],
                                                                  estimation[1],
                                                                  estimation[2]),
                               args.work_on_loop, args.log_file)
            if not args.no_like_follow:
                followings = data['api'].getTotalSelfFollowings()
                user = random.choice(followings)
                ih.results_log(user['username'], args.work_on_loop, args.log_file)
                res = ih.user_followers_like_follow_helper(data, user['pk'],
                                                           args.user_count,
                                                           args.likes_count,
                                                           (args.min_estimate,
                                                            args.max_estimate))
                ih.results_log(res, args.work_on_loop, args.log_file)
            should_work = args.work_on_loop 
        time.sleep(50)
                

if __name__ == '__main__':
    # use parser to get parameters from command line
    parser = argparse.ArgumentParser(
        description='Helper for instagram. Can unfolow not folowers,'
                    'like and follow new users that can help you with'
                    'profile boosting.')
    parser.add_argument('--username', help='your username', default='')
    parser.add_argument('--password', help='your password', default='')
    parser.add_argument('--unfollow', help='Flag to unfollow not followers',
                        action='store_true')
    parser.add_argument('--estimate', help='Flag to estimate your'
                        ' profile (fraction followings/followers)',
                        action='store_true')
    parser.add_argument('--no_like_follow', help='Flag to not like and follow',
                        action='store_true')
    parser.add_argument('--user_count', help='How many users like and'
                        ' follow', type=int, default=25)
    parser.add_argument('---likes_count', help='How many likes give'
                        ' to users', type=int, default=10)
    parser.add_argument('--min_estimate', help='min estimation value'
                        ' for following user', type=float, default=0.7)
    parser.add_argument('--max_estimate', help='max estimation value'
                        ' for following user', type=float, default=1.2)
    parser.add_argument('--work_on_loop', action='store_true',
                        help='Flag to continuously working.')
    parser.add_argument('--start_hour', type=int, default=0,
                        help='Hour to start helper job.')
    parser.add_argument('--start_min', type=int, default=0,
                        help='Minutes to start helper job.')
    parser.add_argument('--log_file', type=str, default='log_helper.log')
    args = parser.parse_args()
    main(args)
