from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from functions import get_puuid, get_name_and_tag, get_match_history, get_match_data_from_id # Importe get_match_history

load_dotenv()
app = Flask(__name__)
CORS(app)

RIOT_API_KEY = os.getenv('riot_api_key')

@app.route('/api/summoner', methods=['POST'])
def get_summoner_puuid_route():
    try:
        data = request.get_json()
        summoner_name_with_tag = data.get('summonerName')
        if not summoner_name_with_tag:
            return jsonify({'error': 'Nome de invocador não fornecido!'}), 400

        api_key = os.getenv('riot_api_key')
        if not api_key:
            return jsonify({'error': 'Chave da API da Riot não configurada!'}), 500

        if "#" not in summoner_name_with_tag:
            return jsonify({'error': 'Formato de nome de invocador inválido. Use Nome#Tag'}), 400

        summoner, tag = summoner_name_with_tag.split("#")
        puuid = get_puuid(gameName=summoner, tagLine=tag, api_key=api_key)

        if puuid:
            return jsonify({'puuid': puuid}), 200
        else:
            return jsonify({'error': 'Invocador não encontrado com essa tag!'}), 404

    except Exception as e:
        return jsonify({'error': f'Erro interno no servidor ao buscar PUUID: {str(e)}'}), 500

@app.route('/api/user/profile/<puuid>', methods=['GET'])
def get_user_profile(puuid):
    try:
        api_key = os.environ.get('riot_api_key')
        if not api_key:
            return jsonify({'error': 'Chave da API da Riot não configurada!'}), 500

        summoner_data = get_name_and_tag(puuid=puuid, api_key=api_key)
        if not summoner_data:
            return jsonify({'error': f'Dados básicos do invocador para o PUUID {puuid} não encontrados!'}), 404

        match_ids = get_match_history(region= 'americas', puuid=puuid, start = 0, count = 2)
        if match_ids is None:
            return jsonify({'error': f'Histórico de partidas para o PUUID {puuid} não encontrado!'}), 500
        
        match_details_list = []
        for match_id in match_ids:
            match_data = get_match_data_from_id(region='americas', matchId=match_id, api_key=api_key, puuid_alvo=puuid)
            if match_data:
                match_details_list.append(match_data)
            else:
                print(f"Erro ao buscar detalhes do jogador na partida com ID: {match_id}")
                # Lide com falhas conforme necessário

        # Combine os dados do invocador com o histórico de partidas
        profile_data = {
            **summoner_data,
            'matchHistory': match_details_list,
            'SummonerId': match_ids
        }

        return jsonify(profile_data), 200
    

    except Exception as e:
        return jsonify({'error': f'Erro interno no servidor ao buscar perfil: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)