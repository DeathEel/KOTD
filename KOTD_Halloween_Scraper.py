'''
Programmer: Kevin Nguyen
Date: 2023-11-06
Description: Scans comments from a given Reddit URL and gives data on the KOTD Halloween event
'''

import sys
# argument is folder where praw folder is if it is not with executable
sys.path.append("C:/Users/Kevin Nguyen/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages")
import praw
from praw.models import MoreComments

# Known rules/guidelines and their flavour texts here
knownRG = ["Capital", "Vowel", "Boring", "Awkward Length", "Even Buy",
        "37 Characters", "Low Roll", "Critical", "69 Characters", "Troll", "Old Races"]
knownFlav = ["You're getting a", "So many nice", ["Wow. Have you", "Well. That's a"], "I know I", "Why don't you",
        "Birbles would be", "Maybe something sweet", "Looks like the", "Nice.", "Does this candy", "Sometimes it is",
        "I see what"]

def main():
    # Parts taken from https://praw.readthedocs.io/en/stable/tutorials/comments.html
    # Create instance of reddit
    r = praw.Reddit(
        client_id = "AucjjdRQarW-z5Dm34UnzQ",
        client_secret = "tzU0ap3M00W0POHWFWBuKBNqGq1SZQ",
        user_agent = "KOTD Halloween Data Collection (by u/DeathEel)"
    )

    # Ask for submission ID
    submissionID = input("Please provide the boss ID: ")
    
    # Lists and Sets to be used
    rgActive = []
    rgUnsure = []
    rgInactive = []
    rgUntested = []

    commentIDList = []
    commentBodyList = []
    parentIDList = []
    parentBodyList = []
    flavourList = []

    rgCountList = []
    rgSetList = []

    # PHASE 1: USE FLAVOUR TEXT TO FIND ACTIVE RULES/GUIDELINES

    # Retrieve relevant comments and their parents, flavour texts, and rules/guidelines counts
    print("Retrieving comments...")
    commentIDList, commentBodyList, parentIDList, parentBodyList = getComments(r, submissionID)
    flavourList = getFlavourText(commentBodyList, parentBodyList)
    rgCountList = getRGCount(commentBodyList)

    # Find the explicit rule/guideline in flavour text