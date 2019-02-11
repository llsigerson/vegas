#this code cleans up the data collection process in the case of a wifi outage
#first, need to identify tweets that were already processed and tweets that came from retweeters
#so that they don't get reprocessed
#find cutpoint where wifi cut out
cutpoint=76
already_processed_indices= pd.Series(archive.index).apply(lambda x: x in tweets_processed[:cutpoint])
seed_diagnostics= diagnostics.loc[diagnostics.source=="initial seed"]
retweeter_diagnostics= diagnostics.loc[diagnostics.source!="initial seed"]
from_retweeters_indices =archive.user_screen_name.apply(lambda x: retweeter_diagnostics.user.str.contains(x,case=False).any())
keep = [True] * archive.shape[0]
for i in range(archive.shape[0]):
    if already_processed_indices[i] or from_retweeters_indices[i]:
        keep[i]=False
hold_out= [not i for i in keep]

#first_round_held_out= archive.loc[hold_out]
second_round_held_out= archive.loc[hold_out]
#first_round_processed= copy.deepcopy(tweets_processed)
#first_round_held_out= copy.deepcopy(held_out_archive)
#then, run retweet_ expansion again
diagnostics, archive, tweets_processed= vegas.retweet_expansion(diagnostics,archive.loc[keep],num_retweets=num_retweets,api=api,
                                              subset=False, subset_size=subset_size-cutpoint)
archive= pd.concat([archive,first_round_held_out, second_round_held_out])