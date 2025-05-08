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
    if puuid is None or api_key is None:
        print("Erro: PUUID e API Key são necessários para buscar o nome e a tag.")
        return None

    link = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={api_key}'

    try:
        response = requests.get(link)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        data = response.json()
        gameName = data.get('gameName')
        tagLine = data.get('tagLine')
        return {'name': gameName, 'tag': tagLine}
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar nome e tag para PUUID {puuid}: {e}")
        return None
    except ValueError:
        print(f"Erro ao decodificar a resposta JSON para PUUID {puuid}.")
        return None



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



def get_match_history(region=None, puuid=None, start=None, count=None):
    if region is None or puuid is None:
        print("Erro: Região e PUUID devem ser fornecidos para buscar o histórico de partidas.")
        return None

    root_url = f'https://{region}.api.riotgames.com/'
    endpoint = f'/lol/match/v5/matches/by-puuid/{puuid}/ids'
    query_parameters = f'?start={start}&count={count}'
    headers = {
        'X-Riot-Token': api_key
    }
    try:
        response = requests.get(root_url + endpoint + query_parameters, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar histórico de IDs de partidas para {puuid}: {e}")
        return None
    except ValueError:
        print(f"Erro ao decodificar a resposta JSON para o histórico de partidas de {puuid}.")
        return None

#print(get_match_history(region='americas', puuid='1kmJRV8jI0nNHw200ztDz4wmYQ9vdvN_dRIGeOX8iXapkMxGDJ3u7zAEzyWkYSCqXkFzB33y10rr-Q'))

def get_match_data_from_id(region=None, matchId=None, api_key=None, puuid_alvo=None):
    if region is None or matchId is None or api_key is None or puuid_alvo is None:
        print("Erro: Região, ID da partida, API Key e PUUID do alvo devem ser fornecidos.")
        return None

    root_url = f'https://{region}.api.riotgames.com/'
    endpoint = f'/lol/match/v5/matches/{matchId}'

    headers = {
        'X-Riot-Token': api_key
    }

    try:
        response = requests.get(root_url + endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()

        player_stats = next((p for p in data['info']['participants'] if p['puuid'] == puuid_alvo), None)

        if player_stats:
            print(f"Estatísticas do jogador {puuid_alvo} na partida {matchId}: {player_stats['championName']}")
            return player_stats
        else:
            print(f"Jogador com PUUID {puuid_alvo} não encontrado na partida {matchId}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar detalhes da partida {matchId}: {e}")
        return None
    except ValueError:
        print(f"Erro ao decodificar a resposta JSON da partida {matchId}.")
        return None

# Exibir o bloco do jogador
#    if player_stats:    
#        print(player_stats['championName'])
#        return player_stats
#    else:
#        print("Jogador não encontrado")


#print(get_match_data_from_id(region='americas', matchId='BR1_3064652652'))