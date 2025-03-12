from dotenv import load_dotenv
load_dotenv()

import os
import requests
import pandas as pd

#temp
gameName = '1v9machine'
tagLine = '2025'
puuid = '1kmJRV8jI0nNHw200ztDz4wmYQ9vdvN_dRIGeOX8iXapkMxGDJ3u7zAEzyWkYSCqXkFzB33y10rr-Q'
#temp
api_key = os.environ.get('riot_api_key')
region = 'americas'


def get_puuid(gameName=None, tagLine=None, api_key=None):
    link = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}'

    response = requests.get(link)

    return response.json()['puuid']


#get_puuid(gameName=gameName, tagLine=tagLine, api_key=api_key)

def get_name_and_tag(puuid=None, api_key=None):
    link = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={api_key}'

    response = requests.get(link)

    gameName = response.json()['gameName']
    tagLine = response.json()['tagLine']

    return f'{gameName}#{tagLine}'


def get_topchal(api_key, top):

    link = f'https://br1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5'
    topchal_resp = requests.get(link + '?api_key=' + api_key)


    if topchal_resp.status_code != 200:
        return f"Erro ao obter dados: {topchal_resp.status_code}"
        

    topchal_df = pd.DataFrame(topchal_resp.json().get('entries', []))
    topchal_df = topchal_df.sort_values(by='leaguePoints', ascending=False).head(top).reset_index(drop=True)

    topchal_df['Summoner'] = topchal_df['puuid'].apply(lambda puuid: get_name_and_tag(puuid, api_key))

    topchal_df = topchal_df[['Summoner', 'leaguePoints', 'wins', 'losses']]

    topchal_df.index += 1
    
    return topchal_df



def get_match_history(region=None, puuid=None, start = 0, count = 20):
    root_url = f'https://{region}.api.riotgames.com/'
    endpoint = f'/lol/match/v5/matches/by-puuid/{puuid}/ids'
    query_parameters = f'?start={start}&count={count}'
    response = requests.get(root_url + endpoint + query_parameters + '&api_key=' + api_key)

    return response.json()

#print(get_match_history(region='americas', puuid='1kmJRV8jI0nNHw200ztDz4wmYQ9vdvN_dRIGeOX8iXapkMxGDJ3u7zAEzyWkYSCqXkFzB33y10rr-Q'))

def get_match_data_from_id(region=None, matchId=None):
    
    root_url = f'https://{region}.api.riotgames.com/'
    endpoint = f'/lol/match/v5/matches/{matchId}'
    puuid_alvo = get_puuid(gameName=gameName, tagLine=tagLine, api_key=api_key)
    
    response = requests.get(root_url + endpoint + '?api_key=' + api_key)

    data = response.json()
    match_id = data['metadata']['matchId']
    print("Match ID:", match_id)


    player_stats = next((p for p in data['info']['participants'] if p['puuid'] == puuid_alvo), None)

# Exibir o bloco do jogador
    if player_stats:    
        print(player_stats['championName'])
        return player_stats
    else:
        print("Jogador não encontrado")


print(get_match_data_from_id(region='americas', matchId='BR1_3064652652'))