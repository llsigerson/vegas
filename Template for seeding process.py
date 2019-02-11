#This script is a customizable template for the tweet seeding process
#Care should be taken to change variable names if you don't want to write over previous work
import requests
import re
import pandas as pd
import numpy as np
import tweedy
import pendulum
import json
import tweepy
import pytz
import datetime
import random
import tweepy_setup
import vegas
import copy
#Customizable parameters
#first, select which api token you'll be using
api= api1
num_retweets=3
subset_size=500
Keyword= "Pundits"
Title= Keyword+" "+str(datetime.datetime.now().date())


start_time= datetime.datetime.now()

#here initialize the diagnostics and archive dataframes
diagnostics= pd.DataFrame({"user":"example","name":"example","source":"example","uncollectable":False, "followers":0,
                           "num_tweets":0, "orig_tweets":0,"relevant_orig_tweets":0}, index=range(5))[:0]
diagnostics=diagnostics.reindex(columns=["user", "name","source", "uncollectable", "followers",
                                         "num_tweets","orig_tweets","relevant_orig_tweets"])
archive= tweedy.statuses(api.user_timeline("jonfavs"))[:0]
#then, process the accounts list, updating the diagnostics and archive dataframes accordingly
print("Data Collection Phase One:")

for account in accounts:
    print("processing seed", accounts.index(account) + 1,
          "out of", len(accounts), "initial seeds")
    diagnostics, archive= vegas.process_user(account, source="initial seed", diagnostics=diagnostics,
                                              tweets_archive=archive,api=api)

backup_archive=copy.deepcopy(archive)
#next, conduct one round of retweet expansion on these tweets
#write everything to an excel file
filename= Title+".xlsx"
writer=pd.ExcelWriter(filename)

diagnostics.to_excel(writer,"Diagnostics")
#need to clean up the tweet archive before writing it
archive.full_text=archive.full_text.str.replace("amp;","")
#the time zone is converted from UTC (what Twitter returns) to Vegas time,
# then removed so it can be written to excel
archive.created_at= archive.created_at.apply(lambda x: x.tz_convert("America/Los_Angeles").replace(tzinfo=None))

#sort tweet archive by date (earliest tweets first)
archive.sort_values(by="created_at",inplace=True)

archive.to_excel(writer,"Tweet Archive")
writer.save()
end_time= datetime.datetime.now()
time_taken= round((end_time-start_time).seconds/3600,2)


