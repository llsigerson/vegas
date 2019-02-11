def sql_format(df):
    """gets a tweepy dataframe ready for storage in sql"""
    #first, find columns with dictionaries and convert them to json strings
    mod=copy.deepcopy(df)
    for i in range(mod.shape[1]):
        column=mod.iloc[:,i]
        if column.apply(lambda x: type(x)==dict).any():
            mod.iloc[:,i]= column.apply(json.dumps)
        #if column.apply(lambda x: type(x)=="datetime64").any()
    if "created_at" in mod.columns:
        mod.created_at= mod.created_at.astype(datetime.datetime)
    return mod

def count_rows(dbconnection, table):
    """just counts the total rows in an SQL table."""
    #IMPORTANT: the table argument must be a string version of the table name
    return dbconnection.execute("SELECT COUNT(*) FROM "+ table).scalar()