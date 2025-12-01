import { Link } from 'react-router-dom';
import UserMenu from '@/components/UserMenu.jsx';
import './Home.css';

export default function Home() {
  return (
    <div className="home-page">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <Link to="/" className="logo">
            <span className="logo-icon">🎙️</span>
            <span className="logo-text">Kokoro TTS</span>
          </Link>
          <div className="nav-links">
            <a href="#features" className="nav-link">Fonctionnalités</a>
            <a href="#pricing" className="nav-link">Tarifs</a>
            <Link to="/generate" className="nav-link">Générer</Link>
            <UserMenu />
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <span>✨</span>
            <span>Synthèse vocale de nouvelle génération</span>
          </div>
          <h1 className="hero-title">
            Transformez du texte en
            <span className="gradient-text"> voix réaliste en 1 clic</span>
          </h1>
          <p className="hero-description">
            Créez des voix de qualité professionnelle en quelques secondes. 
            Notre technologie avancée utilise l'IA pour générer des voix 
            naturelles et expressives à partir de n'importe quel texte.
            <strong> Gratuit, rapide et sans inscription.</strong>
          </p>
          <div className="hero-actions">
            <Link to="/generate" className="cta-button primary">
              <span>Essayer maintenant</span>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </Link>
            <a href="#how-it-works" className="cta-button secondary">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 18.3333C14.6024 18.3333 18.3333 14.6024 18.3333 10C18.3333 5.39763 14.6024 1.66667 10 1.66667C5.39763 1.66667 1.66667 5.39763 1.66667 10C1.66667 14.6024 5.39763 18.3333 10 18.3333Z" stroke="currentColor" strokeWidth="1.5"/>
                <path d="M10 6.66667V10L12.5 12.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
              <span>Voir comment ça marche</span>
            </a>
          </div>
          <div className="hero-stats">
            <div className="stat-item">
              <div className="stat-number">100%</div>
              <div className="stat-label">Gratuit</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">&lt;30s</div>
              <div className="stat-label">Génération</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">∞</div>
              <div className="stat-label">Utilisations</div>
            </div>
          </div>
        </div>

        <div className="hero-visual">
          <div className="floating-card card-1">
            <div className="card-icon">🎤</div>
            <div className="card-text">Voix naturelle</div>
          </div>
          <div className="floating-card card-2">
            <div className="card-icon">⚡</div>
            <div className="card-text">Génération rapide</div>
          </div>
          <div className="floating-card card-3">
            <div className="card-icon">🎨</div>
            <div className="card-text">Qualité premium</div>
          </div>
        </div>
      </section>

      {/* Pourquoi c'est cool - Bénéfices */}
      <section id="why-cool" className="benefits-section">
        <div className="section-header">
          <h2 className="section-title">Pourquoi c'est cool ?</h2>
          <p className="section-subtitle">
            Découvrez les avantages de notre solution de synthèse vocale
          </p>
        </div>
        <div className="benefits-grid">
          <div className="benefit-card">
            <div className="benefit-icon">🚀</div>
            <h3 className="benefit-title">Rapide et efficace</h3>
            <p className="benefit-description">
              Générez vos fichiers audio en quelques secondes. Plus besoin d'attendre des heures pour produire du contenu audio.
            </p>
          </div>
          <div className="benefit-card">
            <div className="benefit-icon">💰</div>
            <h3 className="benefit-title">100% gratuit</h3>
            <p className="benefit-description">
              Aucun coût caché, aucune limite d'utilisation. Créez autant de voix que vous le souhaitez, gratuitement.
            </p>
          </div>
          <div className="benefit-card">
            <div className="benefit-icon">🎯</div>
            <h3 className="benefit-title">Qualité professionnelle</h3>
            <p className="benefit-description">
              Des voix naturelles et expressives qui rivalisent avec les meilleures solutions payantes du marché.
            </p>
          </div>
          <div className="benefit-card">
            <div className="benefit-icon">🔒</div>
            <h3 className="benefit-title">Sécurisé et privé</h3>
            <p className="benefit-description">
              Vos données sont protégées. Aucune information n'est stockée ni partagée. Confidentialité garantie.
            </p>
          </div>
          <div className="benefit-card">
            <div className="benefit-icon">🎨</div>
            <h3 className="benefit-title">Facile à utiliser</h3>
            <p className="benefit-description">
              Interface intuitive, pas besoin d'être un expert. Créez des voix professionnelles en quelques clics.
            </p>
          </div>
          <div className="benefit-card">
            <div className="benefit-icon">📱</div>
            <h3 className="benefit-title">Accessible partout</h3>
            <p className="benefit-description">
              Utilisez notre service depuis n'importe quel appareil, à tout moment. Aucune installation requise.
            </p>
          </div>
        </div>
      </section>

      {/* Comment ça marche */}
      <section id="how-it-works" className="how-it-works-section">
        <div className="section-header">
          <h2 className="section-title">Comment ça marche ?</h2>
          <p className="section-subtitle">
            Trois étapes simples pour créer votre voix
          </p>
        </div>
        <div className="steps-container">
          <div className="step-item">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3 className="step-title">Saisissez votre texte</h3>
              <p className="step-description">
                Entrez le texte que vous souhaitez convertir en voix. Vous pouvez écrire jusqu'à 500 caractères.
              </p>
            </div>
            <div className="step-icon">✍️</div>
          </div>
          <div className="step-arrow">→</div>
          <div className="step-item">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3 className="step-title">Générez la voix</h3>
              <p className="step-description">
                Cliquez sur "Générer" et notre IA transforme votre texte en voix naturelle en quelques secondes.
              </p>
            </div>
            <div className="step-icon">🎙️</div>
          </div>
          <div className="step-arrow">→</div>
          <div className="step-item">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3 className="step-title">Téléchargez votre audio</h3>
              <p className="step-description">
                Écoutez le résultat et téléchargez votre fichier audio au format WAV de haute qualité.
              </p>
            </div>
            <div className="step-icon">⬇️</div>
          </div>
        </div>
        <div className="how-it-works-cta">
          <Link to="/generate" className="cta-button primary">
            <span>Essayer maintenant</span>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </Link>
        </div>
      </section>

      {/* Fonctionnalités */}
      <section id="features" className="features-section">
        <div className="section-header">
          <h2 className="section-title">Fonctionnalités</h2>
          <p className="section-subtitle">
            Tout ce dont vous avez besoin pour créer des voix professionnelles
          </p>
        </div>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🎤</div>
            <h3 className="feature-title">Synthèse vocale avancée</h3>
            <p className="feature-description">
              Technologie d'IA de pointe pour générer des voix naturelles et expressives à partir de texte.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3 className="feature-title">Génération rapide</h3>
            <p className="feature-description">
              Obtenez vos fichiers audio en quelques secondes grâce à notre infrastructure optimisée.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3 className="feature-title">Haute qualité audio</h3>
            <p className="feature-description">
              Export en format WAV de haute qualité pour une utilisation professionnelle.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3 className="feature-title">Sécurité et confidentialité</h3>
            <p className="feature-description">
              Vos données sont protégées et vos fichiers audio sont générés de manière sécurisée.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💡</div>
            <h3 className="feature-title">Interface intuitive</h3>
            <p className="feature-description">
              Design moderne et facile à utiliser, accessible à tous, même sans compétences techniques.
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🌐</div>
            <h3 className="feature-title">Accessible partout</h3>
            <p className="feature-description">
              Utilisez notre service depuis n'importe quel navigateur, sur tous vos appareils.
            </p>
          </div>
        </div>
      </section>

      {/* Tarification */}
      <section id="pricing" className="pricing-section">
        <div className="section-header">
          <h2 className="section-title">Tarification</h2>
          <p className="section-subtitle">
            Simple, transparent et gratuit
          </p>
        </div>
        <div className="pricing-container">
          <div className="pricing-card featured">
            <div className="pricing-badge">Gratuit</div>
            <div className="pricing-header">
              <h3 className="pricing-title">Plan Gratuit</h3>
              <div className="pricing-price">
                <span className="price-amount">0€</span>
                <span className="price-period">/toujours</span>
              </div>
            </div>
            <ul className="pricing-features">
              <li className="pricing-feature">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M16.6667 5L7.50004 14.1667L3.33337 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <span>Génération illimitée</span>
              </li>
              <li className="pricing-feature">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M16.6667 5L7.50004 14.1667L3.33337 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <span>Qualité audio professionnelle</span>
              </li>
              <li className="pricing-feature">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M16.6667 5L7.50004 14.1667L3.33337 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <span>Aucune inscription requise</span>
              </li>
              <li className="pricing-feature">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M16.6667 5L7.50004 14.1667L3.33337 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <span>Téléchargement illimité</span>
              </li>
              <li className="pricing-feature">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M16.6667 5L7.50004 14.1667L3.33337 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <span>Support communautaire</span>
              </li>
            </ul>
            <Link to="/generate" className="pricing-cta">
              Commencer gratuitement
            </Link>
          </div>
        </div>
        <p className="pricing-note">
          💡 Notre service est entièrement gratuit. Aucun paiement, aucune carte bancaire requise.
        </p>
      </section>

      {/* Témoignages / Confiance */}
      <section id="trust" className="trust-section">
        <div className="section-header">
          <h2 className="section-title">Ils nous font confiance</h2>
          <p className="section-subtitle">
            Découvrez ce que nos utilisateurs pensent de notre service
          </p>
        </div>
        <div className="testimonials-grid">
          <div className="testimonial-card">
            <div className="testimonial-content">
              <div className="testimonial-stars">⭐⭐⭐⭐⭐</div>
              <p className="testimonial-text">
                "Service incroyable ! J'ai pu créer des voix pour mes podcasts en quelques minutes. La qualité est vraiment professionnelle."
              </p>
            </div>
            <div className="testimonial-author">
              <div className="author-avatar">👤</div>
              <div className="author-info">
                <div className="author-name">Alexandre M.</div>
                <div className="author-role">Créateur de contenu</div>
              </div>
            </div>
          </div>
          <div className="testimonial-card">
            <div className="testimonial-content">
              <div className="testimonial-stars">⭐⭐⭐⭐⭐</div>
              <p className="testimonial-text">
                "Gratuit et efficace ! Parfait pour mes besoins. L'interface est intuitive et les résultats sont impressionnants."
              </p>
            </div>
            <div className="testimonial-author">
              <div className="author-avatar">👤</div>
              <div className="author-info">
                <div className="author-name">Sophie L.</div>
                <div className="author-role">Développeuse</div>
              </div>
            </div>
          </div>
          <div className="testimonial-card">
            <div className="testimonial-content">
              <div className="testimonial-stars">⭐⭐⭐⭐⭐</div>
              <p className="testimonial-text">
                "Je l'utilise régulièrement pour mes vidéos YouTube. Rapide, gratuit et de qualité. Que demander de plus ?"
              </p>
            </div>
            <div className="testimonial-author">
              <div className="author-avatar">👤</div>
              <div className="author-info">
                <div className="author-name">Thomas D.</div>
                <div className="author-role">Youtuber</div>
              </div>
            </div>
          </div>
        </div>
        <div className="trust-badges">
          <div className="trust-badge">
            <div className="badge-icon">🔒</div>
            <div className="badge-text">Sécurisé</div>
          </div>
          <div className="trust-badge">
            <div className="badge-icon">⚡</div>
            <div className="badge-text">Rapide</div>
          </div>
          <div className="trust-badge">
            <div className="badge-icon">✅</div>
            <div className="badge-text">Fiable</div>
          </div>
          <div className="trust-badge">
            <div className="badge-icon">🆓</div>
            <div className="badge-text">100% Gratuit</div>
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="final-cta-section">
        <div className="final-cta-content">
          <h2 className="final-cta-title">Prêt à créer vos voix ?</h2>
          <p className="final-cta-subtitle">
            Commencez dès maintenant, c'est gratuit et sans inscription
          </p>
          <Link to="/generate" className="cta-button primary large">
            <span>Essayer maintenant</span>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-grid">
            <div className="footer-column">
              <div className="footer-logo">
                <span className="logo-icon">🎙️</span>
                <span className="logo-text">Kokoro TTS</span>
              </div>
              <p className="footer-description">
                Transformez votre texte en voix naturelle avec notre technologie d'IA avancée.
              </p>
            </div>
            <div className="footer-column">
              <h4 className="footer-title">Navigation</h4>
              <ul className="footer-links">
                <li><Link to="/">Accueil</Link></li>
                <li><a href="#features">Fonctionnalités</a></li>
                <li><a href="#how-it-works">Comment ça marche</a></li>
                <li><a href="#pricing">Tarifs</a></li>
                <li><Link to="/generate">Générer</Link></li>
              </ul>
            </div>
            <div className="footer-column">
              <h4 className="footer-title">Ressources</h4>
              <ul className="footer-links">
                <li><a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a></li>
                <li><a href="#trust">Témoignages</a></li>
                <li><a href="#pricing">Tarification</a></li>
              </ul>
            </div>
            <div className="footer-column">
              <h4 className="footer-title">Légal</h4>
              <ul className="footer-links">
                <li><a href="#privacy">Confidentialité</a></li>
                <li><a href="#terms">Conditions d'utilisation</a></li>
                <li><a href="#contact">Contact</a></li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© 2024 Kokoro TTS. Propulsé par l'IA. Tous droits réservés.</p>
            <p className="footer-note">Service gratuit et open source</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
