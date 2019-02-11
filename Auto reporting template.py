#This template can be used for reporting the results of the seeding process.
#This section goes through the steps in the tracking data table, providing the needed
#result for each step.
#first, define the diagnostics and archive dataframes that the report will be based on
diagnostics= diagnostics
archive= archive

#make special dataframes for reporting
#diagnostics dataframes
seed_diagnostics= diagnostics.loc[diagnostics.source=="initial seed"]
retweeter_diagnostics= diagnostics.loc[diagnostics.source!="initial seed"]

#archive dataframes
seed_archive_indices=archive.user_screen_name.apply(lambda x: seed_diagnostics.user.str.contains(x,case=False).any())
seed_tweets= archive.loc[seed_archive_indices]

#Then build notes for each step
Overview = "Start time: "+ str(start_time.replace(microsecond=0))+ " Processing time:" \
           " "+ str(time_taken)+ " hours"+" Number of retweets checked: "+str(num_retweets)

Step1="Identified "+ str(seed_diagnostics.shape[0])+ " accounts found through ____." \
                                                                    " " +str(seed_diagnostics.shape[0]-seed_diagnostics.uncollectable.sum())+" " \
                                                                                                                   "were collectable."

Step2= "Collected a total of " +str(seed_diagnostics.num_tweets.sum())+" tweets. Hit the max collectable tweets for" \
                                                                  " "+str(seed_diagnostics.shape[0]-(seed_diagnostics.num_tweets>3100).value_counts()[0])+ " users" \
                                                                    " ("+"{:.2%}".format(1-(seed_diagnostics.num_tweets>3100).value_counts(normalize=True)[0])+")"

Step3= str(seed_diagnostics.orig_tweets.sum())+ " of these tweets were original, "+str('{:.2%}'.format(seed_diagnostics.orig_tweets.sum()/seed_diagnostics.num_tweets.sum())+ " of the total")

Step4= str(seed_diagnostics.relevant_orig_tweets.sum())+ " of these original tweets were relevant," \
                                                         " "+str('{:.2%}'.format(seed_diagnostics.relevant_orig_tweets.sum()/seed_diagnostics.orig_tweets.sum()))

# identify total number of retweeters (accounting for num retweets and subsetting)
total_retweeters=np.sum([num_retweets if num>num_retweets else num for num in list(seed_tweets.retweet_count)])
Step5= "Identified "+str(total_retweeters)+" total retweeters"

#calculate number and proportion of duplicate accounts
duplicate_retweeters= total_retweeters-retweeter_diagnostics.shape[0]
Step6= "Removed "+ str(duplicate_retweeters)+ " duplicate retweeters ("+str('{:.2%}'.format(duplicate_retweeters/total_retweeters))+" of " \
                                                                            "the total), leaving "+ str(retweeter_diagnostics.shape[0])+" distinct " \
                                                                            "retweeters. "+str(retweeter_diagnostics.uncollectable.sum())+" were uncollectable."

Step7= "Collected a total of " +str(retweeter_diagnostics.num_tweets.sum())+" tweets. Hit the max collectable tweets for" \
                                                                  " "+str((retweeter_diagnostics.num_tweets>3100).value_counts()[1])+ " users" \
                                                                    " ("+"{:.2%}".format((retweeter_diagnostics.num_tweets>3100).value_counts(normalize=True)[1])+")"

Step8= str(retweeter_diagnostics.orig_tweets.sum())+ " of these tweets were original," \
                                " "+str('{:.2%}'.format(retweeter_diagnostics.orig_tweets.sum()/retweeter_diagnostics.num_tweets.sum())+ " of the total")


Step9= str(retweeter_diagnostics.relevant_orig_tweets.sum())+ " of these original tweets were relevant," \
                                                         " "+str('{:.2%}'.format(retweeter_diagnostics.relevant_orig_tweets.sum()/retweeter_diagnostics.orig_tweets.sum()))

Step10= "The final archive includes "+ str(archive.shape[0])+ " relevant, original tweets " \
                                             "from "+ str(len(archive.user_screen_name.unique()))+" different users."

#then, knit the steps together into the report dataframe and write it to excel
report= pd.DataFrame({"Result":[Overview,Step1,Step2,Step3,Step4,Step5,Step6,Step7,Step8,Step9,Step10]})
report.to_excel("Seeding results report.xlsx")
