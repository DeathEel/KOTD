'''
Programmer: Kevin Nguyen
Date: 2023-12-19
Date Last Modified: 2023-12-19
Description: A set of useful KOTD-specific Reddit scraping functions
Update Log:
2023-12-31  Added findBossesTime
'''

import praw
from datetime import datetime

def reddit(user_agent):
    return praw.Reddit(
        client_id = "AucjjdRQarW-z5Dm34UnzQ",
        client_secret = "tzU0ap3M00W0POHWFWBuKBNqGq1SZQ",
        user_agent = user_agent + " (by u/DeathEel)"
    )

def retrieveComments(submission, sort = "new", commentLimit = 0, replaceMoreLimit = 32):
    submission.comment_sort = sort # sort by ___
    if (commentLimit != 0):
        submission.comment_limit = commentLimit # reduces comment list to ___ comments
    submission.comments.replace_more(limit=replaceMoreLimit)   # replace up to ___ MoreComments instances
    ''' DEBUG to print commentLimit
    print("submission.comment_limit: " + str(submission.comment_limit))  #'''

    return submission.comments.list()

# Find a boss using submission ID
def findBosses(reddit, submissionID):
    return reddit.submission(id=submissionID)

def findBossesTime(reddit, submissionLimit, timeFilter, before):
    bossList = []
    submissionList = reddit.subreddit("kickopenthedoor").new(limit=submissionLimit)
    i = 1
    print("\nBosses to scan:" + "\n" +
          "----------//----------//----------")

    for submission in submissionList:
        if (before):
            if (int(datetime.fromtimestamp(submission.created_utc).timestamp()) < timeFilter):
                try:
                    print(str(i) + ") " + submission.id + ": " + submission.title.split("[Health:")[0] + "\n" +
                      " " * len(str(i) + ") ") + "         " + submission.link_flair_text)
                except:
                    print("Unexpected title or flair")
                    print(submission.title)

                bossList.append(submission)
                i += 1
        else:
            if (int(datetime.fromtimestamp(submission.created_utc).timestamp()) > timeFilter):
                try:
                    print(str(i) + ") " + submission.id + ": " + submission.title.split("[Health:")[0] + "\n" +
                      " " * len(str(i) + ") ") + "         " + submission.link_flair_text)
                except:
                    print("Unexpected title or flair")
                    print(submission.title)

                bossList.append(submission)
                i += 1
    
    print("")

    return bossList

def findBossesTitle(reddit, submissionLimit, titleFilter, whitelist):
    bossList = []
    submissionList = reddit.subreddit("kickopenthedoor").new(limit=submissionLimit)
    i = 1
    print("\nBosses to scan:" + "\n" +
          "----------//----------//----------")

    for submission in submissionList:
        if (whitelist):
            if (titleFilter in submission.title):
                try:
                    print(str(i) + ") " + submission.id + ": " + submission.title.split("[Health:")[0] + "\n" +
                      " " * len(str(i) + ") ") + "         " + submission.link_flair_text)
                except:
                    print("Unexpected title or flair")
                    print(submission.title)
                    
                bossList.append(submission)
                i += 1
        else:
            if (not titleFilter in submission.title):
                try:
                    print(str(i) + ") " + submission.id + ": " + submission.title.split("[Health:")[0] + "\n" +
                      " " * len(str(i) + ") ") + "         " + submission.link_flair_text)
                except:
                    print("Unexpected title or flair")
                    print(submission.title)
                    
                bossList.append(submission)
                i += 1
    
    print("")

    return bossList

def findBossesFlair(reddit, submissionLimit, flairFilter, whitelist):
    bossList = []
    submissionList = reddit.subreddit("kickopenthedoor").new(limit=submissionLimit)
    i = 1

    for submission in submissionList:
        if (whitelist):
            if (flairFilter in submission.link_flair_text):
                print(str(i) + ") " + submission.id + ": " + submission.title.split("[Health:")[0] + "\n" +
                      " " * len(str(i) + ") ") + "         " + submission.link_flair_text)
                bossList.append(submission)
                i += 1
        else:
            if (not flairFilter in submission.link_flair_text):
                print(str(i) + ") " + submission.id + ": " + submission.title.split("[Health:")[0] + "\n" +
                      " " * len(str(i) + ") ") + "         " + submission.link_flair_text)
                bossList.append(submission)
                i += 1

    return bossList
