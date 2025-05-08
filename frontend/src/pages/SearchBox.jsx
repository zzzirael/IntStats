import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Importe useNavigate

const SearchBox = () => {
  const [summonerName, setSummonerName] = useState('');
  const navigate = useNavigate(); // Inicialize useNavigate

  const handleSearch = async () => {
    try {
      console.log('SummonerName digitado:', summonerName);

      const response = await fetch('http://localhost:5000/api/summoner', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ summonerName }),
      });

      if (!response.ok) {
        const errorData = await response.json();  
        throw new Error(errorData.error || 'Erro ao buscar invocador');
      }

      const data = await response.json();
      console.log('Dados do invocador:', data);

      if (data && data.puuid) {
        navigate(`/profile/${data.puuid}`); // Redireciona para a página de perfil com o puuid
      } else {
        alert('PUUID não encontrado na resposta do servidor.');
      }
    } catch (error) {
      console.error('Erro:', error);
      alert(error.message);
    }
  };

  return (
    <div className="search-box">
      <input
        type="text"
        placeholder="Digite o nome do invocador#TAG"
        value={summonerName}
        onChange={(e) => setSummonerName(e.target.value)}
      />
      <button onClick={handleSearch}>Buscar</button>
    </div>
  );
};

export default SearchBox;