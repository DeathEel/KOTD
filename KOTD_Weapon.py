'''
Programmer: Kevin Nguyen
Date: 2023-12-31
Date Last Modified: 2023-12-31
Description: Scrapes weapon min and max damage
Update Log:
YYYY-MM-DD  Updates
            Updates
'''

import KOTD

def main():
    # create instance of reddit
    r = KOTD.reddit("KOTD Weapon Damage Scraper")

    # find all bosses to look at and add to list
    # look for after 2023-10-31
    bossList = KOTD.findBossesTime(r, 2048, 1698735600, False)

    # modify as needed
    idStats = {
        "Holy Moly Skipper Abuse" : [12, 12],
        "Spookie Dookie Skipper Abuse" : [12, 12],
        "Moon Moon Skipper Abuse" : [12, 12],
        "Phyrexian Skipper Abuse" : [12, 12],
        "We didn't start the Skipper Abuse" : [12, 12],
        "Sunburnt Skipper Abuse" : [12, 12],
        "Free Range Skipper Abuse" : [12, 12],
        "Drippy Skipper Abuse" : [12, 12],
        "Category 5 Skipper Abuse" : [12, 12],
        "Pocket Sand Skipper Abuse" : [12, 12],
        "Tricky Bonk" : [4.5, 4.5],
        "Tricky Pew Pew" : [4.5, 4.5],
        "Tricky Zap Zap" : [4.5, 4.5],
        "Treat Filled Hammer" : [10.5, 10.5],
        "Treat Filled Blow-dart" : [10.5, 10.5],
        "Treat Filled Magic Bean" : [10.5, 10.5]
    }

    for b in bossList:
        ''' DEBUG to test a specific boss
        if (b.id != "18umxor"): # boss ID to be tested goes here
            continue    #'''

        print("----------//----------//----------")
        try:
            print(str(bossList.index(b) + 1) + ") " + b.id + ": " + b.title.split("[Health:")[0] + "\n" +
                " " * len(str(bossList.index(b) + 1) + ") ") + "         " + b.link_flair_text)
        except:
            print("Non-boss title or flair")
            print(b.title)
        
        # retrieve at most 2048 comments sorted by new
        ''' DEBUG to time KOTD.retrieveComments()
        print("KOTD.retrieveComments() called\n")  #'''
        comments = KOTD.retrieveComments(b, "new", 0, 0)
        ''' DEBUG to count comments
        print("Comment count: " + str(len(comments)) + "\n") #'''

        # c is comment, an instance of comment class
        for c in comments:
            # ignore non-bot comments
            if (c.author != "KickOpenTheDoorBot"):
                continue

            for id in idStats:
                idMin = idStats[id][0]
                idMax = idStats[id][1]
                # look for keyword
                if (id in c.body):
                    # compare values if possible
                    try:
                        idDamage = int(c.body.split(id)[0].split("+")[-1])
                    except:
                        print("Non-attack bot reply")
                        print(c.body)
                        continue

                    # update values
                    idMin = idDamage if idDamage < idMin else idMin
                    idMax = idDamage if idDamage > idMax else idMax
                    idStats[id][0] = idMin
                    idStats[id][1] = idMax

                    # print feedback
                    print("Min damage for " + id + " is " + str(idMin))
                    print("Max damage for " + id + " is " + str(idMax) + "\n")


    print(idStats)

main()