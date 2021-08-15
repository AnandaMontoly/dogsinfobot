import praw
import time
import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from config import *

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
                
def run_bot(r):
    subredditName = config_data["subreddit"]
    print("waiting on comments")
    for comment in r.subreddit(subredditName).stream.comments(skip_existing=True):
        if comment.author != r.user.me():
            #go through all of the comments
            for command in config_data["commands"]:
                    if run_command(comment, command):
                        print("replied successfully")


if __name__ == "__main__":
        with open ("config.yaml", "r") as f:
                config_data = load(f.read(), Loader=Loader)
                r = bot_login()

        while True:
                run_bot(r)


