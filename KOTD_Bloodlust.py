'''
Programmer: Kevin Nguyen
Date: 2023-12-13
Date Last Modified: 2023-12-13
Description: Finds players with Bloodlust status
Update Log:
YYYY-MM-DD  Updates
            Updates
'''

import KOTD
import math
from datetime import datetime, timedelta

def main():
    # create instance of reddit
    r = KOTD.reddit("KOTD Bloodlust Finder")

    # find all bosses to look at and add to list
    bossList = KOTD.findBossesTitle(r, 40, "[Slime Only]", False)

    bloodlustGainList = []
    bloodlustLossList = []
    for b in bossList:
        ''' DEBUG to test a specific boss
        if (b.id != "18n50nr"): # boss ID to be tested goes here
            continue    #'''

        print("----------//----------//----------\n" +
              str(bossList.index(b) + 1) + ") " + b.id + ": " + b.title.split("[Health:")[0] + "\n" +
              " " * len(str(bossList.index(b)) + ") ") + "         " + b.link_flair_text + "\n")

        # retrieve at most 2048 comments sorted by new
        ''' DEBUG to time KOTD.retrieveComments()
        print("KOTD.retrieveComments() called\n")  #'''
        comments = KOTD.retrieveComments(b, "new", 0, 0)
        ''' DEBUG to count comments
        print("Comment count: " + str(len(comments)) + "\n") #'''

        # find comments where players gained and lost bloodlust
        bloodlustGainList.extend(findBloodlustGain(b, comments))
        bloodlustLossList.extend(findBloodlustLoss(b, comments))

    # combine both to create one list of active bloodlust and account for time
    bloodlustList = reduceBloodlustList(sortBloodlustList(bloodlustGainList), sortBloodlustList(bloodlustLossList))

    # print out players with bloodlust
    printBloodlustList(bloodlustList)

    # gracefully exit
    input("Press Enter to quit\n")

def findBloodlustGain(boss, comments):
    bloodlustList = []
    
    # don't look in live bosses; no bloodlust gain there
    if ("[❤️:" in boss.link_flair_text):
        print("This boss is still alive\n")
        return bloodlustList

    # c is comment, an instance of comment class
    for c in comments:
        # ignore non-bot comments
        if (c.author != "KickOpenTheDoorBot"):
            continue

        # look for keyword
        if ("+**Bloodlust**" in c.body):
            c = c.parent()
            # check for deleted comments
            author = "[deleted]" if c.author is None else c.author.name
            print(author + " gained bloodlust at " + datetime.fromtimestamp(c.created_utc).strftime("%d/%m, %H:%M:%S"))
            bloodlustList.append((author, c.created_utc))
        
        # look for the killing blow; no more bloodlust gain afterwards
        if ("+1 Kill" in c.body):
            break

    print("")
    ''' DEBUG to check for comment loss
    if (not finished):
        print("Could not find the kill\n")  #'''

    return bloodlustList

def findBloodlustLoss(boss, comments):
    bloodlustList = []
    
    # don't look in bosses above 300 HP; no bloodlust loss there
    if ("[❤️:" in boss.link_flair_text):
        if (int(boss.link_flair_text.split("/")[0].split(":")[1]) >= 300):
            print("Boss health threshold not reached\n")
            return bloodlustList

    # c is comment, an instance of comment class
    for c in comments:
        # ignore non-bot comments
        if (c.author != "KickOpenTheDoorBot"):
            continue

        # look for keyword
        if ("2.0x Bloodlust" in c.body):
            c = c.parent()
            # check for deleted comments
            author = "[deleted]" if c.author is None else c.author.name
            print(author + " lost bloodlust at " + datetime.fromtimestamp(c.created_utc).strftime("%d/%m, %H:%M:%S"))
            bloodlustList.append((author, c.created_utc))
        
        # look for health threshold (300); no more bloodlust loss beforehand
        ''' DEBUG to look for threshold in comments
        if ("Boss HP Remaining!" in c.body):
            print("Comment:")
            print(c.body.split(" Boss HP Remaining!")[0].split("\n")[-1])   #'''
        if ("Boss HP Remaining!" in c.body and int(c.body.split(" Boss HP Remaining!")[0].split("\n")[-1]) > 300):
            finished = True
            break

    print("")
    ''' DEBUG to check for comment loss
    if (not finished):
        print("Could not find the threshold\n") #'''

    return bloodlustList

def reduceBloodlustList(gainList, lossList):
    # first check for usage
    for loss in lossList:
        found = False
        lossTime = datetime.fromtimestamp(loss[1])
        lossTimeString = datetime.fromtimestamp(loss[1]).strftime("%d/%m, %H:%M:%S")
        ''' DEBUG to see what loss is being checked
        print("Checking " + loss[0], lossTimeString)  #'''
        for gain in gainList:
            gainTime = datetime.fromtimestamp(gain[1])
            gainTimeString = datetime.fromtimestamp(gain[1]).strftime("%d/%m, %H:%M:%S")
            # check name match
            if (loss[0] != gain[0] or loss[0] == "[deleted]"):
                continue

            # check timestamp less than 12 hours ahead
            if (gainTime +  timedelta(hours=12) < lossTime or loss[1] < gain[1]):
                continue

            # first match is correct
            ''' DEBUG to see what was removed
            print("At " + lossTimeString + ", " + loss[0] + " used their bloodlust gained at " + gainTimeString)  #'''
            found = True
            del gainList[gainList.index(gain)]
            break

        ''' DEBUG to see where bloodlust is not seen gained
        if (not found):
            print("Bloodlust was gained on a lost boss")    #'''

    # second check for loss
    nowTime = datetime.now()
    nowTimeString = datetime.now().strftime("%d/%m, %H:%M:%S")
    nowTimeStamp = math.floor(float(datetime.now().timestamp()))
    ''' DEBUG to see the time now
    print("The time now is " + nowTimeString + "\n")    #'''
    reducedList = []
    for gain in gainList:
        gainTime = datetime.fromtimestamp(gain[1])
        gainTimeString = datetime.fromtimestamp(gain[1]).strftime("%d/%m, %H:%M:%S")
        ''' DEBUG to see time difference
        print("For " + gain[0])
        print("Time now is " + str(nowTimeStamp) + " or " + nowTimeString)
        print("Gain time is " + str(gain[1]) + " or " + gainTimeString)
        print("Time difference is " + str(nowTimeStamp - gain[1]) +
              " or " + (gainTime + timedelta(hours=12)).strftime("%d:%H:%M:%S") + "\n") #'''
        # if 12 hours has passed since bloodlust gained, remove it from list
        if (gainTime + timedelta(hours=12) < nowTime):
            ''' DEBUG to see what was removed
            print("At " + (gainTime + timedelta(hours=12)).strftime("%d/%m, %H:%M:%S") + ", " + gain[0] + " lost their bloodlust gained at " + gainTimeString + "\n")   #'''
            continue

        reducedList.append(gain)

    return reducedList

def sortBloodlustList(list):
    ''' DEBUG to print sorted list
    for bloodlust in sorted(list, key=lambda timestamp: timestamp[1]):
        print(bloodlust[0], datetime.fromtimestamp(bloodlust[1]).strftime("%d/%m, %H:%M:%S"))
    print("")   #'''
    return sorted(list, key=lambda timestamp: timestamp[1])

def printBloodlustList(list):
    print("----------//----------//----------")
    for bloodlust in list:
        print(bloodlust[0] + " loses bloodlust at " + (datetime.fromtimestamp(bloodlust[1]) + timedelta(hours=12)).strftime("%d/%m, %H:%M:%S"))
    
    print("")

main()