import React, { useState } from 'react';

const SearchBox = () => {
  const [summonerName, setSummonerName] = useState('');

  const handleSearch = () => {
    // Lógica para buscar o invocador
    console.log(`Buscando invocador: ${summonerName}`);
  };

  return (
    <div className="search-box">
      <input
        type="text"
        placeholder="Digite o nome do invocador"
        value={summonerName}
        onChange={(e) => setSummonerName(e.target.value)}
      />
      <button onClick={handleSearch}>Buscar</button>
    </div>
  );
};

export default SearchBox;