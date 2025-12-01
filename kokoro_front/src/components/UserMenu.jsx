import { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import './UserMenu.css';

export default function UserMenu() {
  const { user, logout, isAuthenticated } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  if (!isAuthenticated) {
    return (
      <div className="user-menu">
        <Link to="/login" className="nav-link cta-nav">
          Login
        </Link>
        <Link to="/register" className="nav-link cta-nav">
          Sign in
        </Link>
      </div>
    );
  }

  const userInitials = user?.email?.charAt(0).toUpperCase() || 'U';

  return (
    <div className="user-menu" ref={menuRef}>
      <button
        className="user-menu-button"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Menu utilisateur"
      >
        <div className="user-avatar">
          {userInitials}
        </div>
        <span className="user-email">{user?.email}</span>
        <svg
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="none"
          className={`user-menu-arrow ${isOpen ? 'open' : ''}`}
        >
          <path
            d="M4 6L8 10L12 6"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      {isOpen && (
        <div className="user-menu-dropdown">
          <div className="user-menu-header">
            <div className="user-menu-avatar">{userInitials}</div>
            <div className="user-menu-info">
              <div className="user-menu-name">{user?.name || user?.email}</div>
              <div className="user-menu-email">{user?.email}</div>
            </div>
          </div>
          <div className="user-menu-divider"></div>
          <Link
            to="/generate"
            className="user-menu-item"
            onClick={() => setIsOpen(false)}
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path
                d="M10 2.5L2.5 7.5V10C2.5 14.1421 5.85786 18.3333 10 18.3333C14.1421 18.3333 17.5 14.1421 17.5 10V7.5L10 2.5Z"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <span>Générer</span>
          </Link>
          <div className="user-menu-divider"></div>
          <button
            className="user-menu-item user-menu-item-danger"
            onClick={() => {
              logout();
              setIsOpen(false);
            }}
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path
                d="M7.5 17.5H4.16667C3.72464 17.5 3.30072 17.3244 2.98816 17.0118C2.67559 16.6993 2.5 16.2754 2.5 15.8333V4.16667C2.5 3.72464 2.67559 3.30072 2.98816 2.98816C3.30072 2.67559 3.72464 2.5 4.16667 2.5H7.5M13.3333 14.1667L17.5 10M17.5 10L13.3333 5.83333M17.5 10H7.5"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <span>Se déconnecter</span>
          </button>
        </div>
      )}
    </div>
  );
}

