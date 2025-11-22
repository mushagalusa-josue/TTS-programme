import { useState } from 'react';
import axios from 'axios';
import './App.css';

export default function App() {
  const [text, setText] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    const trimmed = text.trim();
    if (!trimmed) {
      setError('Veuillez entrer du texte avant de lancer la synthèse.');
      return;
    }

    setLoading(true);
    setError('');
    setAudioUrl('');

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/tts',
        { text: trimmed },
        { timeout: 150000 } // 150 secondes (2.5 minutes) pour laisser le temps à la génération
      );
      const filename = response.data.audio_file;
      setAudioUrl(`http://127.0.0.1:8000${filename}`);
    } catch (err) {
      console.error('Erreur lors de la génération de la synthèse vocale:', err);
      if (err.response?.status === 504) {
        setError('La génération prend trop de temps. Essayez avec un texte plus court ou réessayez dans quelques instants.');
      } else if (err.response?.status === 500) {
        setError('Erreur serveur lors de la génération. Veuillez réessayer.');
      } else if (err.code === 'ECONNABORTED' || err.message.includes('timeout')) {
        setError('La requête a pris trop de temps. Veuillez réessayer avec un texte plus court.');
      } else {
        setError('Une erreur est survenue. Merci de réessayer.');
      }
    } finally {
      setLoading(false);
    }
  };

  const remainingChars = 500 - text.length;
  const hasText = text.trim().length > 0;

  return (
    <div className="page">
      <div className="card">
        <div className="hero">
          <span className="badge">Synthèse vocale</span>
          <h1>Transformez votre texte en voix naturelle</h1>
          <p>
            Tapez jusqu’à 500 caractères et obtenez un fichier audio prêt à être téléchargé
            en quelques secondes.
          </p>
        </div>

        <div className="form-group">
          <label htmlFor="tts-input">Texte à synthétiser</label>
          <textarea
            id="tts-input"
            rows={6}
            maxLength={500}
            placeholder="Entrez le texte à synthétiser ici..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <div className="input-meta">
            <span className={remainingChars < 50 ? 'warning' : ''}>
              {remainingChars} caractères restants
            </span>
            {hasText && (
              <span>
                {text.trim().split(/\s+/).length} mots
              </span>
            )}
          </div>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <button
          className="primary-btn"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="spinner" />
              Génération en cours...
            </>
          ) : (
            <>
              <span role="img" aria-hidden="true">🎧</span>
              Générer la synthèse vocale
            </>
          )}
        </button>

        {audioUrl && (
          <div className="audio-preview">
            <h2>Prévisualisation</h2>
            <audio controls src={audioUrl} />
            <a className="download-link" href={audioUrl} download="tts-output.wav">
              Télécharger le fichier audio
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
