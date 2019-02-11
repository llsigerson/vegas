#I've read in local accounts before this
accounts= accounts[1:5]
#did step 1 and 2 in data processing in other script, created backup_archive before phase 2
backup_archive.id.apply(lambda x: (archive.id!=x).all()).value_counts()

#reset archive and logistics so that they only have data from phase one
archive= copy.deepcopy(backup_archive)
diagnostics=diagnostics.loc[diagnostics.source=="initial seed"]
