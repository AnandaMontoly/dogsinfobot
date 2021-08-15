import praw
import time
import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from config import *
print(username)
print(password)
print(client_id)

def bot_login():
        #put this in env variables
	r = praw.Reddit(username = username,
				password = password,
				client_id = client_id,
				client_secret = client_secret,
				user_agent = user_agent)

	return r

def run_command(comment, response_dict):
        if response_dict["text"] in comment.body and (response_dict["flair"]=="" or response_dict["flair"] == comment.author_flair_text):
                if response_dict["asReply"]==True:
                        newComment = comment.reply(response_dict["response"])
                        print("replied to comment for "+response_dict["text"]+" command")
                else:
                        newComment = comment.submission.reply(response_dict["response"])
                        print("replied to post")
                if response_dict["sticky"]==True:
                        newComment.mod.distinguish(sticky=True)
                return True
        else:
                return False
                
#right now, I'm going to make it so the bot can only reply to a post with an info sheet once. I think this makes
#the most sense since it has to sticky that post. in order to increase the amount of times it could reply to a post,
#there would probably need to be heroku postgres to prevent repeats without a lot of memory expenditure.
#this would increase the cost and maintenance difficulty of running the bot. my goal is to make a quick to deploy and cheap/easy to update bot

def run_bot(r, comments_replied_to):
    subreddit = config_data["subreddit"]
    print("Searching last 1,000 comments")
    for comment in r.subreddit(subreddit).comments(limit=1000):
        if comment.submission.id not in submissions_replied_to:# and comment.author != r.user.me()
            print(comment.submission.id, submissions_replied_to)
            #go through all of the comments
            for command in config_data["commands"]:
                    #only stop replying to the post if one of the comments is replied to
                    if run_command(comment, command):
                            submissions_replied_to.append(comment.submission.id)
                            with open ("submissions_replied_to.txt", "a") as f:
                                    f.write(comment.submission.id + "\n")
    print("Sleeping for 10 seconds...")
    time.sleep(10)

def get_saved_comments():
	if not os.path.isfile("submissions_replied_to.txt"):
		submissions_replied_to = []
	else:
		with open("submissions_replied_to.txt", "r") as f:
			submissions_replied_to = f.read()
			submissions_replied_to = submissions_replied_to.split("\n")
			submissions_replied_to = filter(None, submissions_replied_to)

	return list(submissions_replied_to)

if __name__ == "__main__":
        with open ("config.yaml", "r") as f:
                config_data = load(f.read(), Loader=Loader)
                r = bot_login()
                submissions_replied_to = get_saved_comments()
                print(submissions_replied_to)

        while True:
                run_bot(r, submissions_replied_to)


