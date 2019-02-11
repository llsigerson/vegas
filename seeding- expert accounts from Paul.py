
#Here, read in the accounts (from a doc, or web, or whatever) and store them in a list called accounts
with open("Accounts from Paul (mod2).txt", encoding= "UTF8") as f:
    lines=f.read().splitlines()
#build accounts list from lines
expert_names = list()
accounts = list()
for line in lines:
    if "@" in line:
        expert_names.append(re.findall("[A-Za-z0-9 .]*", line)[0])
        accounts.append(re.findall("\@[A-Za-z0-9_]*", line)[0])
for x in range(len(accounts)):
    accounts[x]= accounts[x].replace("@", "")

