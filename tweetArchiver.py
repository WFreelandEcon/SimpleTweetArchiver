# tweetArchiver.py
#
# Quickly archive your tweets to a plain text file.
#
# This script is limited to retrieving only your
# 3,200 most recent tweets (you have twitter
# to thank for that)
#
# Created by: Tim Bueno
# Website: http://www.timbueno.com
#
# USAGE: python tweetArchiver.py

import tweepy
import codecs
import pytz

utc = pytz.utc

# Archive file location
archiveFile = "/Users/timbueno/Desktop/logDir/twitter.txt"
theUserName = 'timbueno'
homeTZ = pytz.timezone('US/Eastern')

# Create Twitter API Object
api = tweepy.API()

# helpful variables
status_list = [] # Create empty list to hold statuses
cur_status_count = 0 

# Request first status page from twitter
statuses = api.user_timeline(count=200, include_rts=True, screen_name=theUserName)
# Get User information for display
theUser = statuses[0].author
total_status_count = theUser.statuses_count
print "- - - - - - - - - - - - - - - - -"
print "- Archiving "+theUser.name+"'s tweets"
print "- Archive file:"
print "- " + archiveFile
print "-"
print "- http://www.timbueno.com"
print "- - - - - - - - - - - - - - - - -"

while statuses != []:
    cur_status_count = cur_status_count + len(statuses)
    for status in statuses:
        status_list.append(status)
    
    # Get tweet id from last status in each page
    theMaxId = statuses[-1].id
    theMaxId = theMaxId - 1
    
    # Get new page of statuses based on current id location
    statuses = api.user_timeline(count=200, include_rts=True, max_id=theMaxId, screen_name=theUserName)
    print "%d of %d tweets processed..." % (cur_status_count, total_status_count)

print "- - - - - - - - - - - - - - - - -"
print "Total Statuses Retrieved: " + str(len(status_list))
print "Writing statuses to log file:"

f = codecs.open(archiveFile, 'a', 'utf-8')
for status in reversed(status_list):
    theTime = utc.localize(status.created_at).astimezone(homeTZ)
    f.write(status.text + '\n')
    f.write(theTime.strftime("%B %d, %Y at %I:%M%p\n"))
    f.write('http://twitter.com/'+status.author.screen_name+'/status/'+str(status.id)+'\n')
    f.write('- - - - - \n\n')

f.close()

print "Finished!"
print "- - - - - - - - - - - - - - - - -"