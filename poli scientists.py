
#Here, read in the accounts (from a doc, or web, or whatever) and store them in a list called accounts
with open("Poli scientists.txt") as f:
    lines=f.read().splitlines()
#build accounts list from lines
accounts = list()
for line in lines:
    if "@" in line:
        accounts.append(re.findall("\@[A-Za-z0-9_]*", line)[0])
for x in range(len(accounts)):
    accounts[x]= accounts[x].replace("@", "")

