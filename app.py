import streamlit as st
import requests
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import numpy as np


headers = { 'X-Auth-Token': 'bb8615aa6f3541c89c59790cbbc41be6' }


st.title('World Football Leagues Dashboard')
st.sidebar.title('Widget Section')

apilink = '[Football Data](https://www.football-data.org/)'
githublink = '[GitHub Repo](https://github.com/himanshu004/World-Football-Leagues-Dashboard)'
with st.sidebar.beta_expander('About the project'):
    st.write('The idea behind this project was motivated by my love for football and curiosity for stats. This project uses RESTful API provided by ',apilink,' which provides football data and statistics (live scores, fixtures, tables, squads, lineups/subs, etc.) in a machine-readable way.')
    st.write('Want to contribute?',githublink)

#api request 1
@st.cache(persist = True)
def fetch_data1():
    url = "http://api.football-data.org/v2/competitions/"
    # querystring = {'areas':[1,2]}
    response = requests.request("GET", url, headers = headers,)
    return response.json()

data = fetch_data1()

area_dict = {}
comp_dict = {}
for i in range(len(data['competitions'])):
    area_dict[data['competitions'][i]['area']['name']] = 0
    comp_dict[data['competitions'][i]['name']] = 0


for i in range(len(data['competitions'])):
    area_dict[data['competitions'][i]['area']['name']] += 1
    comp_dict[data['competitions'][i]['name']] += 1


area_df = pd.DataFrame(area_dict.items(), columns=['Country Name', 'Count'])
comp_df = pd.DataFrame(comp_dict.items(), columns=['League Name','Count'])

newwc = st.sidebar.button('New Wordcloud!',key = 1)
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

show_comp_stats = st.sidebar.checkbox('Country Wise Distribution',key = 1)

if(show_comp_stats):
    st.header('Number Of Competitions Per Country:')
    space = '\n'
    st.write(space)
    chosen_nations = st.sidebar.multiselect('Choose Country',area_df['Country Name'],key = 1)
    sub_area_df = area_df[area_df['Country Name'].isin(chosen_nations)]
    st.write(sub_area_df)
    st.write(space)
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

show_leagues_per_country = st.sidebar.checkbox('Football Leagues By Country',key = 2)

if(show_leagues_per_country):
    country = st.sidebar.selectbox('Choose Country',area_df['Country Name'],key = 2,)
    write = country + '\'s football leagues: '
    st.header(write)
    st.write(space)
    country_list = []
    for i in range(len(data['competitions'])):
        if(data['competitions'][i]['area']['name'] == country):
            country_list.append(data['competitions'][i]['name'])
    for i in range(len(country_list)):
        st.subheader((country_list[i]))


    
