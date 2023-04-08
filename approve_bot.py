from meczbot import subreddit

comments = subreddit.stream.comments(skip_existing=False)

for comment in comments:
    if comment.author == 'meczbot':
        comment.mod.approve()