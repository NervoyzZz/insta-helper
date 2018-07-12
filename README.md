# Insta Helper
I have an Instagram profile and I noticed that I do same actions every day. So I decided to automate this process.
## Unfollow users
First of all I don't want to follow guys that don't follow me. Maybe in future I'll want to subscribe some users that can not follow me but not now.
use `--unfollow=1` as command line argument to clean up your followings list.
## Profile estimation
I want to know my followings/followers coefficient. So use `--estimate=1` as command line argument to know this coef.
## Profile boosting
Main part of my script is auto-like and auto-follow users. So script choose random guy from your followings and go to his followers. 
Then it choose some random guys from list and gives them likes and follows them. But not every gyu will be followed. Script estimate every profile
and then decide to only-like user or like-follow him. For example if user has a lot of followers and a litle bit followings chance that he will follow
you is tiny, so let's only-like him. Another example if user follow a lot of men but has not enough followers you has chance that he will follow you
without your following and it's defence from trading-accounts. Also, script save users that you've already followed or that followed you.

use `--user_count` to set count of user that you want to like-follow. `--like_count` to set count of likes for every selected user. 
`--min_estimate` to set low border for followings and `max_estimate` to set high border for followings.

## Requires
To make this script work you should install InstagramAPI by LevPasha. It's unofficial Instagram API. Use `pip3 install InstagramAPI` to install this api.
And of course you should have Python3. And Instagram pfrofile is required too.

## Project structure
There two files `ih_functions.py` with functions and `insta_helper.py` with main script. insta_helper is demo app, so you can use every function from ih_functions
too create your own helper. Script will create `*.api` file with information of your user and not-follow-users-list. 

## What's next
I want to improve application, to add more functions to boost account, but I can tell you now what I will add next.

## Any help
Feel free to use my code according to license. Any ideas and additionals are welcome!

### Nepryahin Daniil 2018