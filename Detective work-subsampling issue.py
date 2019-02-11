#read in subsampled data
filename='Local (subsampled) 2018-12-14.xlsx'
sub_sampled_archive= pd.read_excel(filename, sheet_name=1)

#read in tweets that were cut in the subsampling
missing_archive= pd.read_excel("missing tweets.xlsx")

#find diagnostics (note, I had to shift the sheets in the file first)
diagnostics= pd.read_excel(filename, sheet_name=1)