import flatten_dict as fd
import pandas as pd
import numpy as np
import json
import re
import datetime
import pytz
import copy

def dictval_to_list(column, key):
    """takes a column of dictionaries and outputs a list of certain values in the dicts"""
    #if there's a nan instead of a dict, output a nan
    output = [entry[key] if type(entry) is dict else np.nan for entry in column]
    return output

def dict_check(dataframe):
    #takes a dataframe and checks which columns have any dictionaries in them
    return dataframe.apply(lambda x: (x.apply(type)==dict).any())

def time_check(dataframe):
    #takes a dataframe and checks which columns have any datetime objects in them
    return dataframe.apply(lambda x: (x.apply(type)==datetime.datetime).any())


def rate_limit(authentication):
    #load in data as a dictionary of dictionaries
    init_data= json.loads(json.dumps(authentication.rate_limit_status()))
    #flatten to a single dictionary with a tuple for each key
    init_data= fd.flatten(d=init_data["resources"], reducer="tuple")
    #create a list of the keys (tuples) for easy iteration later
    key_list = list(init_data.keys())

    #initialize empty dataframe that'll be added to iteratively row by row
    data= pd.DataFrame({"Type":[],"Resource":[], "Limit": [], "Remaining":[], "Reset":[]})
    #build the dataframe
    for key in key_list:
        if key[2]== "limit":
            data=data.append({"Type": key[0] ,"Resource": key[1], "Limit": init_data[key], "Remaining":np.nan,
                          "Reset":np.nan}, ignore_index=True)
        elif key[2] == "remaining":
            data.loc[data.Resource==key[1],"Remaining"]= init_data[key]
        elif key[2] == "reset":
            data.loc[data.Resource == key[1], "Reset"] = init_data[key]
    #add a logical column just to indicate whether the resource has been used at all
    data["Used"]= data.Limit>data.Remaining
    return data

def users(tweepy_output):
    """takes tweepy user info output and converts it to a handy dataframe"""
    jsons= json.loads(json.dumps(tweepy_output._json))
    df= pd.DataFrame(jsons)
    # set the indices to be the unique user ids
    df.index = df.id_str
    df=df.drop("id_str", axis=1)
    df.created_at = list(map(lambda x: datetime.datetime.strptime(x, "%a %b %d %H:%M:%S %z %Y"), df.created_at))
    return df[:1]

def statuses(tweepy_output):
    """takes tweepy statuses output and converts it to a handy dataframe"""
    jsons= [json.loads(json.dumps(status._json)) for status in tweepy_output]
    df= pd.DataFrame(jsons)
    #set the indices to be the unique tweet ids
    df.index= df.id_str
    df = df.drop("id_str", axis=1)
    #add in a few other helpful columns that are buried in dictionaries in tweepy
    df["user_id"]= dictval_to_list(df.user, "id_str")
    df["user_screen_name"] = dictval_to_list(df.user, "screen_name")

    #convert created_at column to datetime objects
    df.created_at = list(map(lambda x: datetime.datetime.strptime(x,  "%a %b %d %H:%M:%S %z %Y"), df.created_at))
    return df

