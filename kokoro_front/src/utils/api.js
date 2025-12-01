/**
 * Utilitaire pour les appels API avec authentification
 */
import axios from 'axios';

const getApiUrl = () => {
  return (import.meta.env.VITE_API_URL || 'https://kokoro-tts-api-production-b52e.up.railway.app').replace(/\/$/, '');
};

/**
 * Créer une instance axios avec le token d'authentification
 */
export const getAuthenticatedAxios = () => {
  const token = localStorage.getItem('token');
  const API_URL = getApiUrl();
  
  const instance = axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    }
  });
  
  return instance;
};

/**
 * Obtenir l'URL de base de l'API
 */
export const getApiBaseUrl = () => {
  return getApiUrl();
};



