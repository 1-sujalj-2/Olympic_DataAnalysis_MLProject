import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import process,helper_fnc
import plotly.express as px
import seaborn as sns
import plotly.figure_factory as ff

plt.ion()
ath_df = pd.read_csv("athlete_events.csv")
noc_df = pd.read_csv("noc_regions.csv")


new_ath_df = process.processor(ath_df,noc_df)
st.sidebar.header('Olympic Games Analysis(1896-2016)')
st.sidebar.image("https://w7.pngwing.com/pngs/243/351/png-transparent-"
                 "olympic-games-2018-winter-olympics-olympic-medal-olympic-symbols-award-award-ring-medal-logo-thumbnail.png")
menu = st.sidebar.radio(
    'Show',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete-Wise Analysis')
)


medal_df = new_ath_df.drop_duplicates(subset=['Sex', 'Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])

if (menu == 'Medal Tally'):
    st.sidebar.header('Olympics Medal Tally')
    year, country = helper_fnc.list_of_country_year(new_ath_df)

    s_year = st.sidebar.selectbox('Select Year',year)
    s_country = st.sidebar.selectbox('Select Country', country)

    m_tally = helper_fnc.fetch_tally(s_year, s_country, medal_df)
    st.header(f'Year: {str(s_year)} &emsp;' +  f'Country: {s_country}')
    st.table(m_tally)

if (menu == 'Overall Analysis'):
    editions, cities, sports, countries, events, athletes = helper_fnc.oanalysis(new_ath_df)

    st.title('Statistics:')
    c1,c2,c3 = st.columns(3)
    with c1:
        st.header('Editions:')
        st.title(editions)

    with c2:
        st.header('Cities:')
        st.title(cities)

    with c3:
        st.header('Sports:')
        st.title(sports)

    c4, c5, c6 = st.columns(3)
    with c4:
        st.header('Countries:')
        st.title(countries)

    with c5:
        st.header('Events:')
        st.title(events)

    with c6:
        st.header('Athletes:')
        st.title(athletes)

    nation_df = helper_fnc.nation_events(new_ath_df,'region')
    fig = px.line(nation_df, x="Year", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    event_df = helper_fnc.nation_events(new_ath_df,'Event')
    fig1 = px.line(event_df, x="Year", y="Event")
    st.title("Olympic Events over the years")
    st.plotly_chart(fig1)

    athletes_df = helper_fnc.nation_events(new_ath_df, 'Name')
    athletes_df.rename(columns={'Name':'athletes'},inplace=True)
    fig2 = px.line(athletes_df, x="Year", y="athletes")
    st.title("No. of athletes over the years")
    st.plotly_chart(fig2)

    st.title('No. of Events in different Olympic Sports over the years')
    fig3,axes = plt.subplots(figsize=(25, 25), dpi=150)
    sns.heatmap(
        pd.pivot_table(ath_df.drop_duplicates(subset=['Year', 'Event', 'Sport']), columns=['Year'], index='Sport',
                       values='Event', aggfunc='count').fillna(0).astype(int), annot=True,ax=axes)
    st.pyplot(fig3)

    st.title('Athletes\' Performance')
    s_list = new_ath_df['Sport'].unique().tolist()
    s_list.sort()
    s_list.insert(0, 'Overall')
    s_list.insert(0, 'Select')
    s_sport = st.selectbox('Select a Sport',s_list)
    bt = helper_fnc.best(s_sport, new_ath_df)
    bt.reset_index(inplace=True,drop=True)
    st.table(bt)


if (menu == 'Country-Wise Analysis'):
    countries = new_ath_df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, 'Select')
    st.sidebar.title('Country-Wise Analysis')
    s_country = st.sidebar.selectbox('Select a Country', countries)
    cm = helper_fnc.c_mtally(s_country,new_ath_df)
    st.title(f'Medal tally of {str(s_country)} ' + 'over the years:')
    cm.rename(columns={'count':'medals'},inplace=True)
    st.table(cm)
    fig4 = px.line(cm, x="Year", y="medals")
    st.plotly_chart(fig4)

    if(s_country!='Select'):
        st.title(f'{str(s_country)}\'s performance in different Olympic Sports over the years:')
        fig5, axes = plt.subplots(figsize=(25, 25), dpi=150)
        sns.heatmap(helper_fnc.c_hmap(new_ath_df,s_country).astype(int), annot=True, ax=axes)
        st.pyplot(fig5)

    st.title(f'{str(s_country)}\'s Top 10 best performing athletes:')
    st.table(helper_fnc.bestincountry(new_ath_df,s_country)[['Name','total_medals','Sport']])

if (menu == 'Athlete-Wise Analysis'):
    a_df = new_ath_df.drop_duplicates(subset=['Name', 'region', 'Sex'])
    data1 = a_df['Age'].dropna()
    data2 = a_df[a_df['Medal'] == 'Gold']['Age'].dropna()
    data3 = a_df[a_df['Medal'] == 'Silver']['Age'].dropna()
    data4 = a_df[a_df['Medal'] == 'Bronze']['Age'].dropna()


    fig = ff.create_distplot([data1, data2, data3, data4], ['Overall Age', 'Gold', 'Silver', 'Bronze'], show_hist=False,
                             show_rug=False)
    fig.update_layout(autosize=False,width=4000,height=600)

    st.title('Probability of winning medals across different ages:')
    fig.update_layout(xaxis_title='Age',yaxis_title='Probability')
    st.plotly_chart(fig)


    sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
              'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
              'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
              'Water Polo', 'Hockey', 'Rowing', 'Fencing',
              'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
              'Tennis', 'Golf', 'Softball', 'Archery',
              'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
              'Rhythmic Gymnastics', 'Rugby Sevens',
              'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    s_age = []
    s_name = []
    for sport in sports:
        s_df = a_df[a_df['Sport'] == sport]
        s_age.append(s_df[s_df['Medal'] == 'Gold']['Age'].dropna().tolist())
        s_name.append(sport)

    fig1 = ff.create_distplot(s_age, s_name, show_hist=False, show_rug=False)
    fig1.update_layout(autosize=False, width=5000, height=600)

    st.title('Probability of winning gold medal across different ages in different olympic sports:')
    fig1.update_layout(xaxis_title='Age', yaxis_title='Probability')
    st.plotly_chart(fig1)

    s_list = new_ath_df['Sport'].unique().tolist()
    s_list.sort()
    s_list.insert(0, 'Overall')
    s_list.insert(0, 'Select')
    s_sport = st.selectbox('Select a Sport', s_list)
    helper_fnc.plot_hw_sport(a_df,s_sport)

    mf_df = a_df[['Year', 'Sex']].groupby(['Year', 'Sex']).size().reset_index()
    mf_df.rename(columns={0: 'count'}, inplace=True)
    fig2 = px.line(mf_df, x="Year", y="count", color='Sex')
    st.title("No. of Male/Female Athletes over the years")
    st.plotly_chart(fig2)






