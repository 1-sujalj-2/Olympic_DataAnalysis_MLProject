import pandas as pd

def processor(ath_df,noc_df):
    ath_df =ath_df.drop('Games',axis=1)
    ath_df = ath_df[ath_df['Season'] == 'Summer']

    ath_df = ath_df.merge(noc_df[['NOC','region']],on='NOC',how='left')

    ath_df.drop_duplicates(inplace=True)

    ath_df = pd.concat([ath_df,pd.get_dummies(ath_df['Medal'])],axis=1)
    return ath_df