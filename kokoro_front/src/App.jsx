import { useState } from 'react';
import axios from 'axios';
import './App.css';

export default function App() {
  const [text, setText] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!text.trim()) return alert('Veuillez entrer du texte.');
    setLoading(true);
    try {
      // URL de l'API : utilise la variable d'environnement ou l'URL Railway par défaut
      // On enlève le slash final pour éviter les doubles slashes
      const API_URL = (import.meta.env.VITE_API_URL || 'https://kokoro-tts-api-production-b52e.up.railway.app').replace(/\/$/, '');
      
      const response = await axios.post(`${API_URL}/tts`, 
        { text },
        { timeout: 300000 } // 5 minutes pour permettre le téléchargement des modèles
      );
      const filename = response.data.audio_file; 
      setAudioUrl(`${API_URL}${filename}`);
    }
    catch (error) {
      console.error('Erreur lors de la génération de la synthèse vocale:', error);
      if (error.response?.status === 404) {
        alert('Endpoint non trouvé. Vérifiez que l\'URL de l\'API est correcte.');
      } else {
        alert('Une erreur est survenue lors de la génération de la synthèse vocale.');
      }
    }
    finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1> TTS </h1>
      <textarea
        row="5"
        placeholder="Entrez le texte à synthétiser ici..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <br />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Génération en cours...' : 'Générer la synthèse vocale'}
      </button>

      {audioUrl && (
        <div>
          <audio controls src={audioUrl}> </audio>
          <p>
            <a href={audioUrl} download="audio.wav">
              Télécharger le fichier audio
            </a>
          </p>
        </div>
      )} 
    </div>
  );
}

