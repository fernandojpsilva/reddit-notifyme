import praw
import config

# Initialize Reddit PRAW
reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent,
                     username=config.username,
                     password=config.password)

# Get variables from config.py
subreddit = reddit.subreddit(config.subreddit)
search_list = config.search_list
send_to = config.send_to


# Searches for the words listed in config.py 'search_list'
# over the last n posts
# TODO: continuous updating/streaming for new posts
def search_last_posts():
    posts_to_send = []
    n = 5
    for post in subreddit.new(limit=n):
        print(f'{post.title} {post.url}')
        if any(x in post.title for x in search_list):
            posts_to_send.append(post.id)

    return posts_to_send


# Sends private message to user listed in config.py 'send_to'
# with the post(s) link(s)
def send_pm(posts):
    pm_title = subreddit
    pm_body = ''
    for post_id in posts:
        post = reddit.submission(id=post_id)
        pm_body += post.title + ' ' + post.permalink + '\n\n'

    reddit.redditor(send_to).message(pm_title, pm_body)


# main function
def main():
    posts_to_send = search_last_posts()
    send_pm(posts_to_send)


if __name__ == '__main__':
    main()
