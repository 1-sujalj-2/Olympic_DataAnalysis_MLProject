import numpy as np
import pandas as pd
import streamlit
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import streamlit as st

def tally(ath_df):
    new_medal_tally=ath_df.drop_duplicates(subset=['Sex', 'Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal']).groupby('region')[
        ['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index()

    new_medal_tally['Total_medals'] = new_medal_tally['Gold'] + new_medal_tally['Silver'] + new_medal_tally['Bronze']

    return new_medal_tally


def list_of_country_year(ath_df):
    year = np.sort(ath_df['Year'].unique())
    year = year.tolist()
    year.insert(0, 'Overall')
    year.insert(0, 'Select')

    country = np.sort(ath_df['region'].dropna().unique())
    country = country.tolist()
    country.insert(0, 'Overall')
    country.insert(0, 'Select')

    return year, country


def fetch_tally(s_year, s_country,medal_df):
    if ((s_year == 'Overall') & (s_country == 'Overall')):
        fetched_tally = medal_df

    elif ((s_year == 'Overall')):
        fetched_tally = medal_df[(medal_df['region'] == s_country)]

    elif ((s_country == 'Overall')):
        fetched_tally = medal_df[(medal_df['Year'] == s_year)]

    else:
        fetched_tally = medal_df[(medal_df['Year'] == s_year) & (medal_df['region'] == s_country)]

    if ((s_year == 'Overall') & (s_country != 'Overall')):
        per_year_tally = fetched_tally.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year').reset_index()
        streamlit.header('Tally Per Year: &emsp; '+f'Country: {s_country}')
        streamlit.dataframe(per_year_tally)

    fetch_tally = fetched_tally.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold',ascending=False).reset_index()

    fetch_tally['Total'] = fetch_tally['Gold'] + fetch_tally['Silver'] + fetch_tally['Bronze']

    return fetch_tally


def oanalysis(new_ath_df):
    cities = new_ath_df['City'].unique().shape[0]  #no.of cities where olympics were held
    sports = new_ath_df['Sport'].unique().shape[0]  # no. of sports played at the olympics
    countries = new_ath_df['region'].unique().shape[0]  # estimate no.of participating nations
    events = new_ath_df['Event'].unique().shape[0]  # number of events
    atheletes = new_ath_df['Name'].unique().shape[0]  # no. of atheletes
    editions = new_ath_df['Year'].unique().shape[0] - 1    #no. of olympic editions

    return editions,cities,sports,countries,events,atheletes

def nation_events(new_ath_df,col):
    data_df = pd.DataFrame(new_ath_df.drop_duplicates(subset=['Year', col])['Year'].value_counts()).sort_values('Year').reset_index()
    data_df.rename(columns={'count': col}, inplace=True)

    return data_df

def best(spt,new_ath_df):
    op = new_ath_df.dropna(subset=['Medal'])
    n_op = pd.DataFrame(op['Name'].value_counts()).reset_index()
    n_op.rename(columns={'count': 'total_medals'}, inplace=True)
    ath_perf = n_op.merge(op.drop_duplicates('Name')[['Name', 'Sport', 'region']], how='inner', on='Name')
    if(spt=='Overall'):
        return ath_perf
    else:
        return ath_perf[ath_perf['Sport'] == spt]


def c_mtally(country,new_ath_df):
    ct = new_ath_df.drop_duplicates(subset=['Sex', 'Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    ct.dropna(subset=['Medal'], inplace=True)
    cm = pd.DataFrame(ct[ct['region']==country]['Year'].value_counts()).sort_values(by='Year')
    cm.reset_index(inplace=True)
    return cm

def c_hmap(new_ath_df,country):
    ct = new_ath_df.drop_duplicates(subset=['Sex', 'Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    ct.dropna(subset=['Medal'], inplace=True)
    return pd.pivot_table(ct[ct['region'] == country], index='Sport', columns=['Year'], values='Medal', aggfunc='count').fillna(0)


def bestincountry(new_ath_df,country):
    op = new_ath_df.dropna(subset=['Medal'])
    n_op = pd.DataFrame(op['Name'].value_counts()).reset_index()
    n_op.rename(columns={'count': 'total_medals'}, inplace=True)
    ath_perf = n_op.merge(op.drop_duplicates('Name')[['Name', 'Sport', 'region']], how='inner', on='Name')
    return ath_perf[ath_perf['region']==country].reset_index(drop='first').head(10)


def plot_hw_sport(a_df,s_sport):
    a_df['Medal'].fillna('None', inplace=True)
    if(s_sport!='Overall'):
        hw_df = a_df[a_df['Sport'] == s_sport]
    else:
        hw_df = a_df

    fig5, axes = plt.subplots(figsize=(10,10),dpi=200)
    plt.title('Height vs Weight in 'f'{str(s_sport)}')
    axes = sns.scatterplot(x=hw_df['Weight'],y=hw_df['Height'],hue=hw_df['Medal'],style=hw_df['Sex'])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig5)