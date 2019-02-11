#Here, read in the accounts (from NBC News' list)
accounts=[]
for member in tweepy.Cursor(tweepy_setup.api1.list_members, 'NBCNews', 'las-vegas-shooting').items():
    accounts.append(tweedy.users(member).screen_name[0])

