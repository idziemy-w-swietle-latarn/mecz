import praw

reddit = praw.Reddit(client_id = '{{secrets.CLIENT_ID}}',
                     client_secret = '{{secrets.CLIENT_SECRET}}',
                     username = 'meczbot',
                     password = '{{secrets.PASSWORD}}',
                     user_agent = '/r/meczbot /u/meczbot')


subreddit = reddit.subreddit('mecz')




def main():
    pass





if __name__ == '__main___':
    main()