import praw
import os

reddit = praw.Reddit(client_id = os.environ['CLIENT_ID'],
                     client_secret = os.environ['CLIENT_SECRET'],
                     username = 'meczbot',
                     password = os.environ['PASSWORD'],
                     user_agent = '/r/meczbot /u/meczbot')


subreddit = reddit.subreddit('mecz')




def main():
    pass





if __name__ == '__main___':
    main()