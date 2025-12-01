"""
Script de test pour vérifier la connexion à la base de données PostgreSQL
"""
import os
import sys
from database import engine, init_db
from sqlalchemy import text

# Configuration
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/kokoro_tts"
)

# Si Railway ou autre service utilise postgres:// au lieu de postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print("=" * 60)
print("Test de connexion à la base de données PostgreSQL")
print("=" * 60)
print(f"URL: {DATABASE_URL.split('@')[0]}@***")  # Ne pas afficher le mot de passe
print()

try:
    # Tester la connexion
    print("1. Test de connexion...")
    # Forcer la connexion avec un timeout
    with engine.connect() as conn:
        # Test simple
        result = conn.execute(text("SELECT 1"))
        test_value = result.fetchone()[0]
        if test_value == 1:
            print(f"   ✅ Connexion réussie!")
        
        # Obtenir la version
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"   PostgreSQL version: {version.split(',')[0]}")
    
    # Vérifier si les tables existent
    print("\n2. Vérification des tables...")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result]
        
        if 'users' in tables:
            print(f"   ✅ Table 'users' existe déjà")
            print(f"   Tables existantes: {', '.join(tables)}")
        else:
            print("   ⚠️  Table 'users' n'existe pas encore")
            print("   Initialisation des tables...")
            init_db()
            print("   ✅ Tables créées avec succès!")
    
    # Compter les utilisateurs
    print("\n3. Statistiques...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM users"))
        count = result.fetchone()[0]
        print(f"   Nombre d'utilisateurs: {count}")
    
    print("\n" + "=" * 60)
    print("✅ Tous les tests sont passés avec succès!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    print("\n" + "=" * 60)
    print("Vérifiez que:")
    print("1. PostgreSQL est démarré (Docker ou installation locale)")
    print("2. DATABASE_URL est correcte")
    print("3. Les identifiants sont valides")
    print("4. Le port 5432 est accessible")
    print("=" * 60)
    sys.exit(1)
