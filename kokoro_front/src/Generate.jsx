import { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import UserMenu from '@/components/UserMenu.jsx';
import './Generate.css';

export default function Generate() {
  const [text, setText] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!text.trim()) {
      setError('Veuillez entrer du texte avant de lancer la synthèse.');
      return;
    }

    setLoading(true);
    setError('');
    setAudioUrl('');

    try {
      const API_URL = (import.meta.env.VITE_API_URL || 'https://kokoro-tts-api-production-b52e.up.railway.app').replace(/\/$/, '');
      
      const response = await axios.post(`${API_URL}/tts`, 
        { text: text.trim() },
        { timeout: 300000 }
      );
      const filename = response.data.audio_file; 
      setAudioUrl(`${API_URL}${filename}`);
    }
    catch (error) {
      console.error('Erreur lors de la génération de la synthèse vocale:', error);
      let errorMessage = 'Une erreur est survenue lors de la génération de la synthèse vocale.';
      
      if (error.response) {
        const status = error.response.status;
        const detail = error.response.data?.detail || error.response.data?.message || 'Erreur inconnue';
        
        if (status === 404) {
          errorMessage = 'Endpoint non trouvé. Vérifiez que l\'URL de l\'API est correcte.';
        } else if (status === 500) {
          errorMessage = `Erreur serveur: ${detail}`;
        } else if (status === 504) {
          errorMessage = 'La génération prend trop de temps. Essayez avec un texte plus court.';
        } else {
          errorMessage = `Erreur ${status}: ${detail}`;
        }
      } else if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        errorMessage = 'La requête a pris trop de temps. La première génération peut prendre plusieurs minutes (téléchargement des modèles).';
      } else if (error.message) {
        errorMessage = `Erreur: ${error.message}`;
      }
      
      setError(errorMessage);
    }
    finally {
      setLoading(false);
    }
  };

  const remainingChars = 500 - text.length;
  const hasText = text.trim().length > 0;

  return (
    <div className="generate-page">
      <nav className="navbar">
        <div className="nav-container">
          <Link to="/" className="logo">
            <span className="logo-icon">🎙️</span>
            <span className="logo-text">Kokoro TTS</span>
          </Link>
          <div className="nav-links">
            <Link to="/" className="nav-link">Accueil</Link>
            <Link to="/generate" className="nav-link active">Générer</Link>
            <UserMenu />
          </div>
        </div>
      </nav>

      <div className="generate-container py-10">
        <div className="generate-card">
          <div className="card-header">
            <h1 className="card-title">Générer une synthèse vocale</h1>
            <p className="card-subtitle">
              Entrez votre texte ci-dessous et obtenez un fichier audio de haute qualité
            </p>
          </div>

          <div className="form-section">
            <div className="form-group">
              <label htmlFor="tts-input" className="form-label">
                Texte à synthétiser
              </label>
              <textarea
                id="tts-input"
                className="text-input"
                rows={8}
                maxLength={500}
                placeholder="Entrez le texte que vous souhaitez convertir en voix naturelle..."
                value={text}
                onChange={(e) => setText(e.target.value)}
              />
              <div className="input-meta">
                <span className={remainingChars < 50 ? 'warning' : ''}>
                  {remainingChars} caractères restants
                </span>
                {hasText && (
                  <span className="word-count">
                    {text.trim().split(/\s+/).length} mots
                  </span>
                )}
              </div>
            </div>

            {error && (
              <div className="alert alert-error">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M10 18.3333C14.6024 18.3333 18.3333 14.6024 18.3333 10C18.3333 5.39763 14.6024 1.66667 10 1.66667C5.39763 1.66667 1.66667 5.39763 1.66667 10C1.66667 14.6024 5.39763 18.3333 10 18.3333Z" stroke="currentColor" strokeWidth="1.5"/>
                  <path d="M10 6.66667V10M10 13.3333H10.0083" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                <span>{error}</span>
              </div>
            )}

            <button
              className="generate-button"
              onClick={handleSubmit}
              disabled={loading || !text.trim()}
            >
              {loading ? (
                <>
                  <div className="spinner"></div>
                  <span>Génération en cours...</span>
                </>
              ) : (
                <>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M3.33333 10L8.33333 15L16.6667 6.66667" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  <span>Générer la synthèse vocale</span>
                </>
              )}
            </button>
          </div>

          {audioUrl && (
            <div className="audio-section">
              <div className="audio-header">
                <h2 className="audio-title">Votre audio est prêt</h2>
                <p className="audio-subtitle">Écoutez et téléchargez votre fichier audio</p>
              </div>
              <div className="audio-player-container">
                <audio controls className="audio-player" src={audioUrl}>
                  Votre navigateur ne supporte pas la lecture audio.
                </audio>
                <a 
                  href={audioUrl} 
                  download="tts-output.wav" 
                  className="download-button"
                >
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M17.5 12.5V15.8333C17.5 16.2754 17.3244 16.6993 17.0118 17.0118C16.6993 17.3244 16.2754 17.5 15.8333 17.5H4.16667C3.72464 17.5 3.30072 17.3244 2.98816 17.0118C2.67559 16.6993 2.5 16.2754 2.5 15.8333V12.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M5.83333 8.33333L10 12.5L14.1667 8.33333" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M10 12.5V2.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  <span>Télécharger</span>
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

