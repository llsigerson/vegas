
#Here, read in the accounts (from a doc, or web, or whatever) and store them in a list called accounts
url= 'https://en.wikipedia.org/wiki/List_of_most-followed_Twitter_accounts'
r  = requests.get(url)
data = r.text
accounts=re.findall("\@[A-Za-z0-9_]*",data)
accounts = accounts[2:]
accounts=[account.replace("@","") for account in accounts]

