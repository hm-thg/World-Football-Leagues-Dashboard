import streamlit as st
import requests
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import modules as md

githublink = '[GitHub Repo](https://github.com/himanshu004/World-Football-Leagues-Dashboard)'
st.sidebar.write('Contribute here: ' + githublink)

st.title('World Football Leagues Dashboard')
st.sidebar.title('Widget Section')

apilink = '[Football Data](https://www.football-data.org/)'
with st.sidebar.beta_expander('About the project'):
    st.write('The idea behind this project was motivated by my love for football and curiosity for stats. This project uses RESTful API provided by ',apilink,' which provides football data and statistics (live scores, fixtures, tables, squads, lineups/subs, etc.) in a machine-readable way.')
    st.write('Want to contribute?',githublink)

data1 = md.fetch_data1()

area_dict = {}
comp_dict = {}
for i in range(len(data1['competitions'])):
    area_dict[data1['competitions'][i]['area']['name']] = 0
    comp_dict[data1['competitions'][i]['name']] = 0


for i in range(len(data1['competitions'])):
    area_dict[data1['competitions'][i]['area']['name']] += 1
    comp_dict[data1['competitions'][i]['name']] += 1


area_df = pd.DataFrame(area_dict.items(), columns=['Country Name', 'Count'])
comp_df = pd.DataFrame(comp_dict.items(), columns=['League Name','Count'])

newwc = st.sidebar.button('New Wordcloud!',key = 1,)
newwc = True
if(newwc):
    words = ' '.join(comp_df['League Name'])
    wordcloud = WordCloud(stopwords = STOPWORDS, background_color = 'white',width = 820, height = 410).generate(words)
    plt.imshow(wordcloud)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.xticks([])
    plt.yticks([])
    sns.despine(left = True,bottom = True)
    st.pyplot()

newwc = False

st.sidebar.header('General Stats:\n')

show_comp_stats = st.sidebar.checkbox('Country Wise Distribution',key = 1)

if(show_comp_stats):
    st.header('Number Of Competitions Per Country:\n')
    chosen_nations = st.sidebar.multiselect('Choose Country',area_df['Country Name'],key = 1)
    if(len(chosen_nations) == 0):
        st.write('Choose a country..')
    else:    
        sub_area_df = area_df[area_df['Country Name'].isin(chosen_nations)].reset_index().drop(['index'],axis = 1)
        sub_area_df.index = range(1,len(sub_area_df) + 1)
        st.table(sub_area_df)
        st.write('\n')
        if(sub_area_df.shape[0] != 0):
            sns.set_style('whitegrid')
            params = {'legend.fontsize': 18,
                'figure.figsize': (20, 8),
                'axes.labelsize': 22,
                'axes.titlesize': 22,
                'xtick.labelsize': 22,
                'ytick.labelsize': 22,
                'figure.titlesize': 22}
            plt.rcParams.update(params)
            fig, ax = plt.subplots() 
            ax = sns.barplot(data = sub_area_df,x = 'Country Name',y = 'Count')
            if(len(sub_area_df) > 5):
                plt.xticks(rotation = 60)
            if(len(sub_area_df) > 10):
                plt.xticks(rotation = 90)
            sns.despine(left = True)
            st.pyplot(fig)  

show_leagues_per_continent = st.sidebar.checkbox('Football Leagues By Continent',key = 2)

continents = ['Europe','Asia','Africa','North America','South America','Australia']

if(show_leagues_per_continent):
    choice = st.sidebar.selectbox('Choose Continent',continents,key = 2,)
    write = choice + '\'s football leagues: '
    st.header(write + '\n')
    md.leaguesDisplay(choice,data1)

show_leagues_per_country = st.sidebar.checkbox('Football Leagues By Country',key = 3)

if(show_leagues_per_country):
    helper = list(area_df[~area_df['Country Name'].isin(continents)]['Country Name'])
    choice = st.sidebar.selectbox('Choose Country',helper,key = 3,)
    write = choice + '\'s football leagues: '
    st.header(write + '\n')
    md.leaguesDisplay(choice,data1)
    

st.sidebar.header('Competitions Stats:')

comp_dict = {}
free_tier_list = ['Serie A','Premier','UEFA Champions','European','Ligue 1','Bundesliga','Eridivisie','Primeira Liga','Primera Division','FIFA World Cup']

for i in range(len(data1['competitions'])):
    if(data1['competitions'][i]['name'] not in free_tier_list):
        continue
    comp_dict[data1['competitions'][i]['name']] = data1['competitions'][i]['id']

default = 'Select a Competition'
options = [default]

options = options + list(comp_dict.keys())
svalue = st.sidebar.selectbox('',options,key = 4)

if(svalue != default):
    st.title(svalue)   
    if(st.sidebar.checkbox('Team Info')):
        data2 = md.fetch_data2("teams",comp_dict,svalue)
        st.header('Number of teams: ' + str(data2['count']))
        col1, col2 = st.beta_columns(2)
        if(len(data2['teams'])):
            for i in range(len(data2['teams'])):
                if(i % 2):
                    col1.subheader(data2['teams'][i]['name'])
                    if('address' in data2['teams'][i].keys()):
                        col1.write('Address: ' + data2['teams'][i]['address'])
                    if('phone' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['phone'] != None):
                            col1.write('Phone: ' + (data2['teams'][i]['phone']))
                    if('website' in data2['teams'][i].keys()):
                        col1.write('Website: ' + data2['teams'][i]['website'])
                    if('email' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['email'] != None):
                            col1.write('Email: ' + data2['teams'][i]['email'])
                    if('founded' in data2['teams'][i].keys()):
                        col1.write('Founded in ' + str(data2['teams'][i]['founded']))
                    if('venue' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['venue'] != None):
                            col1.write('Venue: ' + data2['teams'][i]['venue'])
                else:
                    col2.subheader(data2['teams'][i]['name'])
                    if('address' in data2['teams'][i].keys()):
                        col2.write('Address: ' + data2['teams'][i]['address'])
                    if('phone' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['phone'] != None):
                            col2.write('Phone: ' + (data2['teams'][i]['phone']))
                    if('website' in data2['teams'][i].keys()):
                        col2.write('Website: ' + data2['teams'][i]['website'])
                    if('email' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['email'] != None):
                            col2.write('Email: ' + data2['teams'][i]['email'])
                    if('founded' in data2['teams'][i].keys()):
                        col2.write('Founded in ' + str(data2['teams'][i]['founded']))
                    if('venue' in data2['teams'][i].keys()):
                        if(data2['teams'][i]['venue'] != None):
                            col2.write('Venue: ' + data2['teams'][i]['venue'])

    if(st.sidebar.checkbox('Standings')):
        st.header('Standings: ')
        data2 = md.fetch_data2("standings",comp_dict,svalue)
        if(svalue != 'FIFA World Cup'):
            type = st.sidebar.radio('',['Total','Home','Away'])
            if(type == 'Total'):
                df = pd.DataFrame()
                for i in range(len(data2['standings'][0]['table'])):
                    list = []
                    list.append(data2['standings'][0]['table'][i]['position']) 
                    list.append(data2['standings'][0]['table'][i]['team']['name'])
                    list.append(data2['standings'][0]['table'][i]['playedGames']) 
                    list.append(data2['standings'][0]['table'][i]['form']) 
                    list.append(data2['standings'][0]['table'][i]['won']) 
                    list.append(data2['standings'][0]['table'][i]['lost']) 
                    list.append(data2['standings'][0]['table'][i]['points']) 
                    list.append(data2['standings'][0]['table'][i]['goalsFor']) 
                    list.append(data2['standings'][0]['table'][i]['goalsAgainst']) 
                    list.append(data2['standings'][0]['table'][i]['goalDifference'])
                    df = df.append(pd.Series(list),ignore_index = True) 
            elif(type == 'Home'):
                df = pd.DataFrame()
                for i in range(len(data2['standings'][1]['table'])):
                    list = []
                    list.append(data2['standings'][1]['table'][i]['position']) 
                    list.append(data2['standings'][1]['table'][i]['team']['name'])
                    list.append(data2['standings'][1]['table'][i]['playedGames']) 
                    list.append(data2['standings'][1]['table'][i]['form']) 
                    list.append(data2['standings'][1]['table'][i]['won']) 
                    list.append(data2['standings'][1]['table'][i]['lost']) 
                    list.append(data2['standings'][1]['table'][i]['points']) 
                    list.append(data2['standings'][1]['table'][i]['goalsFor']) 
                    list.append(data2['standings'][1]['table'][i]['goalsAgainst']) 
                    list.append(data2['standings'][1]['table'][i]['goalDifference']) 
                    df = df.append(pd.Series(list),ignore_index = True) 
            else:
                df = pd.DataFrame()
                for i in range(len(data2['standings'][2]['table'])):
                    list = []
                    list.append(data2['standings'][2]['table'][i]['position']) 
                    list.append(data2['standings'][2]['table'][i]['team']['name'])
                    list.append(data2['standings'][2]['table'][i]['playedGames']) 
                    list.append(data2['standings'][2]['table'][i]['form']) 
                    list.append(data2['standings'][2]['table'][i]['won']) 
                    list.append(data2['standings'][2]['table'][i]['lost']) 
                    list.append(data2['standings'][2]['table'][i]['points']) 
                    list.append(data2['standings'][2]['table'][i]['goalsFor']) 
                    list.append(data2['standings'][2]['table'][i]['goalsAgainst']) 
                    list.append(data2['standings'][2]['table'][i]['goalDifference']) 
                    df = df.append(pd.Series(list),ignore_index = True) 
            df.drop([0],axis = 1,inplace = True)
            df.columns = ['Team Name','Matches Played','Last 5 Matches','Won','Lost','Points','Goals For','Goals Against','Difference']
            df.index = range(1,len(df) + 1)
            st.table(df)
        else:
                for j in range(0,len(data2['standings']),3):
                    df = pd.DataFrame()
                    for i in range(len(data2['standings'][j]['table'])):
                        list = []
                        list.append(data2['standings'][j]['table'][i]['position']) 
                        list.append(data2['standings'][j]['table'][i]['team']['name'])
                        list.append(data2['standings'][j]['table'][i]['playedGames']) 
                        list.append(data2['standings'][j]['table'][i]['form']) 
                        list.append(data2['standings'][j]['table'][i]['won']) 
                        list.append(data2['standings'][j]['table'][i]['lost']) 
                        list.append(data2['standings'][j]['table'][i]['points']) 
                        list.append(data2['standings'][j]['table'][i]['goalsFor']) 
                        list.append(data2['standings'][j]['table'][i]['goalsAgainst']) 
                        list.append(data2['standings'][j]['table'][i]['goalDifference'])
                        df = df.append(pd.Series(list),ignore_index = True) 
                    st.subheader(data2['standings'][j]['group'])
                    df.drop([0],axis = 1,inplace = True)
                    df.columns = ['Team Name','Matches Played','Last 5 Matches','Won','Lost','Points','Goals For','Goals Against','Difference']
                    df.index = range(1,len(df) + 1)
                    st.table(df)
    if(st.sidebar.checkbox('Scorers')):
        data2 = md.fetch_data2('scorers',comp_dict,svalue)
        st.subheader('Top 10 Scorers:')
        df = pd.DataFrame()
        for i in range(len(data2['scorers'])):
            list = []
            list.append(data2['scorers'][i]['player']['name'])
            list.append(data2['scorers'][i]['player']['nationality'])
            list.append(data2['scorers'][i]['player']['position'])
            list.append(data2['scorers'][i]['team']['name'])
            list.append(data2['scorers'][i]['numberOfGoals'])
            df = df.append(pd.Series(list),ignore_index = True)
        df.index = range(1,len(df) + 1)
        df.columns = ['Name','Nationality','Position','Team','Number of Goals']
        st.table(df)

st.sidebar.header('Player Stats:')
st.sidebar.write('Coming soooon!!')




    
