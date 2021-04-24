import requests
import streamlit as st

headers = { 'X-Auth-Token': 'bb8615aa6f3541c89c59790cbbc41be6' }

#api request 1
@st.cache(persist = True)
def fetch_data1():
    url = "http://api.football-data.org/v2/competitions/"
    response = requests.request("GET", url, headers = headers)
    return response.json()

#api request 2
@st.cache(persist = True)
def fetch_data2(param,comp_dict,svalue):
    url = "http://api.football-data.org/v2/competitions/" + str(comp_dict[svalue]) + "/" + param
    response = requests.request("GET", url, headers = headers)
    return response.json()

def leaguesDisplay(choice,data):
    leagues = []
    for i in range(len(data['competitions'])):
        if(data['competitions'][i]['area']['name'] == choice):
            leagues.append(data['competitions'][i]['name'])
    for i in range(len(leagues)):
        st.subheader((leagues[i]))