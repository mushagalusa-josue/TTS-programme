import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

// URL de l'API
const getApiUrl = () => {
  return (import.meta.env.VITE_API_URL || 'https://kokoro-tts-api-production-b52e.up.railway.app').replace(/\/$/, '');
};

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Vérifier si l'utilisateur est connecté au chargement et valider le token
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const storedToken = localStorage.getItem('token');
    
    if (storedUser && storedToken) {
      try {
        const parsedUser = JSON.parse(storedUser);
        // Restaurer l'utilisateur immédiatement depuis le localStorage
        setUser(parsedUser);
        
        // Vérifier que le token est toujours valide en appelant /api/auth/me (en arrière-plan)
        // Ne pas supprimer le token si la validation échoue - le garder pour les prochaines requêtes
        const validateToken = async () => {
          try {
            const API_URL = getApiUrl();
            const response = await axios.get(`${API_URL}/api/auth/me`, {
              headers: {
                'Authorization': `Bearer ${storedToken}`
              }
            });
            // Token valide, mettre à jour les données utilisateur
            setUser(response.data);
            localStorage.setItem('user', JSON.stringify(response.data));
          } catch (error) {
            // Si le token est invalide (401), on garde quand même le token
            // Il sera vérifié lors de la prochaine requête authentifiée
            // Ne logger que les erreurs réseau ou serveur
            if (error.response?.status !== 401 && error.response?.status !== 403) {
              console.warn('Token validation warning:', error.message);
            }
            // Ne pas supprimer le token - le garder pour permettre à l'utilisateur de continuer
            // Le token sera vérifié lors de la prochaine action nécessitant une authentification
          }
        };
        
        // Valider en arrière-plan sans bloquer le chargement
        validateToken();
      } catch (error) {
        console.error('Error parsing user data:', error);
        // Seulement supprimer si les données sont corrompues
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        setUser(null);
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const API_URL = getApiUrl();
      const response = await axios.post(`${API_URL}/api/auth/login`, {
        email,
        password
      });
      
      const { access_token, user: userData } = response.data;
      
      // Stocker le token et les données utilisateur
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);
      
      return { success: true, user: userData };
    } catch (error) {
      console.error('Login error:', error);
      let errorMessage = 'Erreur lors de la connexion';
      
      if (error.response) {
        errorMessage = error.response.data?.detail || errorMessage;
      } else if (error.request) {
        errorMessage = 'Impossible de contacter le serveur';
      }
      
      return { success: false, error: errorMessage };
    }
  };

  const register = async (email, password, name = null) => {
    try {
      const API_URL = getApiUrl();
      const response = await axios.post(`${API_URL}/api/auth/register`, {
        email,
        password,
        name
      });
      
      const { access_token, user: userData } = response.data;
      
      // Stocker le token et les données utilisateur
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);
      
      return { success: true, user: userData };
    } catch (error) {
      console.error('Register error:', error);
      let errorMessage = 'Erreur lors de l\'inscription';
      
      if (error.response) {
        errorMessage = error.response.data?.detail || errorMessage;
      } else if (error.request) {
        errorMessage = 'Impossible de contacter le serveur';
      }
      
      return { success: false, error: errorMessage };
    }
  };

  const logout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}


