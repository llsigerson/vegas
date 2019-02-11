#just contains all the functions needed for my research project with paul on the Las Vegas shooting
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
import tweepy_setup
import random

def remove_retweets(tweets):
    """takes a set of tweets and removes the retweets"""
    return tweets.loc[tweets.retweeted_status.apply(lambda x: type(x)==dict)==False]

def remove_irrelevant(tweets,keywords= ["Paddock", "Mandalay", "Vegas"]):
    """takes a set of tweets and removes the irrelevant retweets"""
    pattern = "|".join(keywords)
    relevant = tweets.full_text.str.contains(pattern, case=False)
    return(tweets.loc[relevant])


#initialize empty statuses df
empty_statuses= tweedy.statuses(tweepy_setup.api1.user_timeline("jonfavs",tweet_mode="extended"))[:0]

def tweets_oct(user, api):
    #gets all tweets after September 30th 2017. May get some earlier tweets as well
    statuses= empty_statuses
    #This cutpoint is set to midnight Sep 30 (Las vegas time), but is in UTC for ease of manipulation
    #All times are converted to las vegas time after data collection and processing
    Cutpoint = pendulum.parse("2017-10-01 07:00:00", strict=False)
    for page in tweepy.Cursor(api.user_timeline, id=user, tweet_mode="extended").pages():
         statuses= pd.concat([statuses, tweedy.statuses(page)])

         if statuses.created_at[-1]<Cutpoint:
             break

    return(statuses.loc[statuses.created_at>Cutpoint])


def process_user(user, source, diagnostics, tweets_archive,api):
    """a highly customized function that takes a user and updates the corresponding dataframes"""
    #warning:only makes sense in the context of this project

    #first, check that the user isn't already in the diagnostics dataframe
    if diagnostics.user.str.contains(user).any():
        #if so, simply return the original dataframes unchanged
        print("it's a duplicate, idiot! Still love you!")
        return diagnostics, tweets_archive
    else:
        try:
            new_tweets_poten1 = tweets_oct(user,api=api)
            new_tweets_poten2 = remove_retweets(new_tweets_poten1)
            new_tweets_final = remove_irrelevant(new_tweets_poten2)
            # add tweets to the archive, and update diagnostics df
            tweets_archive = pd.concat([tweets_archive, new_tweets_final])
            #check the user's number of followers (this is tricky for users with 0 tweets)
            try:
                num_followers= int(new_tweets_poten1.user[0]["followers_count"])
                name= new_tweets_poten1.user[0]["name"]
            except:
                num_followers= tweedy.users(api.get_user(user)).followers_count[0]
                name=tweedy.users(api.get_user(user)).name[0]
            diagnostics = diagnostics.append({"user": user, "name": name,
                                              "source": source,"uncollectable":False,
                                              "followers":num_followers,
                                              "num_tweets": new_tweets_poten1.shape[0],
                                              "orig_tweets": new_tweets_poten2.shape[0],
                                              "relevant_orig_tweets": new_tweets_final.shape[0]}, ignore_index=True)
        except tweepy.error.TweepError as error:
            #if the above process fails, diagnose the problem.
            #Check if the account is uncollectable, and if so, update diagnostics accordingly
            #note, I've checked that this catches private, misspelled (nonexistent), and suspended accounts
            if "Twitter error response: status code" in error.reason:
                diagnostics = diagnostics.append({"user": user, "source": source, "uncollectable": True,
                                              "num_tweets": None,"orig_tweets": None,
                                              "relevant_orig_tweets": None}, ignore_index=True)
            else:
                #otherwise, there's a for real error
                raise Exception("Something broke! Might be the internet connection.\n Time: "+str(datetime.datetime.now()))
        return diagnostics, tweets_archive

def retweet_expansion(diagnostics,tweets_archive, api, num_retweets=3, subset=False, subset_size=300):
    """Takes a set of tweets and searches for additional relevant tweets using retweeting behavior"""

    #check that there are no retweets (you can't retweet a retweet)
    tweets_archive= remove_retweets(tweets_archive)

    #iterate through each tweet and update diagnostics and the archive accordingly
    #First, need to specify which tweets to process in this manner (possibly only a random subset)
    num_seed_tweets = tweets_archive.shape[0]
    if subset:
        subset_amt= (lambda x: x>subset_size and subset_size or x)(num_seed_tweets)
        to_process= random.sample(range(num_seed_tweets),subset_amt)
    else:
        to_process= range(num_seed_tweets)
    #note that this only iterates through the original tweets in the archive, not the ones
    #that are added later
    counter=0
    for tweet_id in tweets_archive.index[to_process]:
        counter+=1
        #every 100 tweets, backup the archive and diagnostics just in case in a seperate folder
        if counter%50==0:
            print("backing up archive and diagnostics")
            backupID=str(random.sample(range(1000),1)[0])
            tweets_archive.to_csv("Interim data collection results/archive "+backupID+".csv")
            diagnostics.to_csv("Interim data collection results/diagnostics " + backupID + ".csv")

        print("processing tweet number ", counter, "out of",
              len(to_process), "seed tweets")
        #try to get retweeters (this will fail if there are no retweets)
        #side note: I'm using a general except to catch this problem, which works. As far as I know,
        #this doesn't catch other errors erroneously
        try:
            # get list of 100 retweeter user_IDs, then remove duplicates
            # note: duplicates appear, possibly because you can "unretweet" and then "reretweet" a tweet
            retweeters= list(set(list(tweedy.statuses(api.retweets(tweet_id,100)).user_screen_name)))
            #if this list is longer than the specified number of retweeters, randomly sample it
            if len(retweeters)>num_retweets:
                retweeters= random.sample(retweeters,num_retweets)
            for retweeter in retweeters:
                #for each retweeter, try to get all their tweets since Oct1.
                # This may fail if the account is private, suspended or deleted
               print("processing retweeter number", retweeters.index(retweeter)+1,
                     "out of", len(retweeters), "retweeters")
               diagnostics, tweets_archive = process_user(user=retweeter,source='tweet: '+tweet_id,
                                         diagnostics=diagnostics,tweets_archive=tweets_archive, api=api)
        except:
            print("no retweets!")
            continue
    #return updated diagnostics and archive, along with the
    # ID's of the tweets that were processed (i.e, checked for retweets)
    return diagnostics, tweets_archive, tweets_archive.index[to_process]






