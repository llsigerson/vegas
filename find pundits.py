#Here, read in the accounts (from Fox News' list)
accounts=[]
for member in tweepy.Cursor(api1.list_members, 'FoxNews', 'shows-hosts').items():
    accounts.append(tweedy.users(member).screen_name[0])

for member in tweepy.Cursor(api1.list_members, 'MSNBC', 'msnbc-hosts').items():
    accounts.append(tweedy.users(member).screen_name[0])
