import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './Profile.css';

const Perfil = () => {
    const { puuid } = useParams();
    const [profileData, setProfileData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [expandedMatch, setExpandedMatch] = useState(null);

    const handleMatchClick = (index) => {
        setExpandedMatch(expandedMatch === index ? null : index);
    };

    useEffect(() => {
        const fetchProfileData = async () => {
            setLoading(true);
            setError(null);
            try {
                const response = await fetch(`http://localhost:5000/api/user/profile/${puuid}`);
                if (response.ok) {
                    const data = await response.json();
                    setProfileData(data);
                } else {
                    const errorData = await response.json();
                    setError(`Erro ao buscar dados do perfil: ${errorData.message || 'Erro desconhecido'}`);
                }
            } catch (error) {
                console.error('Erro ao comunicar com o backend:', error);
                setError('Erro ao comunicar com o servidor.');
            } finally {
                setLoading(false);
            }
        };

        if (puuid) {
            fetchProfileData();
        }
    }, [puuid]);

    if (loading) {
        return <div>Carregando perfil...</div>;
    }

    if (error) {
        return <div>Erro ao carregar o perfil: {error}</div>;
    }

    if (!profileData) {
        return <div>Nenhum dado de perfil encontrado.</div>;
    }

    return (
        <div className="player-stat-page">
            {/* ... (seu cartão de jogador) ... */}

            <div className="matches-container">
                <h3>Partidas Recentes</h3>
                <div className="matches-list">
                    {profileData.matchHistory && profileData.matchHistory.map((matchHistory, index) => (
                        <div
                            key={index} // Como agora cada item é o bloco de estatísticas do jogador
                            className={`match-card ${expandedMatch === index ? 'expanded' : ''}`}
                            onClick={() => handleMatchClick(index)}
                        >
                            <div className="champion-container">
                                {matchHistory.championName && (
                                    <div className="champion-image">
                                        <img
                                            src={`http://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/${matchHistory.championName}.png`}
                                            alt={matchHistory.championName}
                                        />
                                    </div>
                                )}
                                {!expandedMatch && <p className="champion-name">{matchHistory.championName}</p>}
                            </div>

                            {expandedMatch === index && <h2 className="champion-title">{matchHistory.championName}</h2>}

                            <div className="match-summary">
                                <div className="match-result">
                                    <p
                                        className="result"
                                        style={{
                                            color: matchHistory.win ? '#4CAF50' : '#FF4444',
                                        }}
                                    >
                                        {matchHistory.win ? 'Vitória' : 'Derrota'}
                                    </p>
                                    <p className="kda">{matchHistory.kills}/{matchHistory.deaths}/{matchHistory.assists}</p>
                                </div>
                                {/* Adicione outras informações resumidas que você quer mostrar */}
                            </div>

                            {expandedMatch === index && (
                                <div className="match-details">
                                    <p>Nível: {matchHistory.summonerLevel}</p>
                                    <p>CS: {matchHistory.totalMinionsKilled}</p>
                                    {/* Renderize mais detalhes do playerStats conforme necessário */}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Perfil;