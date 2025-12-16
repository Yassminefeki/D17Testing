#!/usr/bin/env python3
"""
config.py — Configuration centralisée du projet D17Testing
Charge et valide toutes les variables depuis .env et fournit des chemins standardisés.
"""

import os
import sys
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ ERREUR: Package 'python-dotenv' non trouvé.")
    print("   Installez-le: pip install python-dotenv")
    sys.exit(1)

# Charger les variables d'environnement
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(env_file)
else:
    print("⚠️ AVERTISSEMENT: Fichier .env non trouvé.")
    print(f"   Copie .env.example → .env et remplissez les valeurs réelles.")


class Config:
    """Classe de configuration centralisée pour le projet."""

    # ===== DÉTERMINATION PATHS =====
    PROJECT_ROOT = Path(__file__).parent.absolute()
    TESTING_DIR = PROJECT_ROOT / "Testing"
    REPORT_DIR = PROJECT_ROOT / "Report"
    SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
    DOCUMENTATION_DIR = PROJECT_ROOT / "DOCUMENTATION"

    # Sous-dossiers Testing
    FUNCTIONAL_TEST_DIR = TESTING_DIR / "Functional_test"
    PERFORMANCE_TEST_DIR = TESTING_DIR / "Performance_Test"
    SECURITY_TEST_DIR = TESTING_DIR / "Security_Test"
    TEST_CASE_GEN_DIR = TESTING_DIR / "Test Case Generate"
    XML_DIR = TESTING_DIR / "XML"

    # Report
    REPORT_JSON_DIR = REPORT_DIR / "report_json"
    REPORT_PDF_DIR = REPORT_DIR / "report_pdf"

    # ===== CONFIGURATION JIRA =====
    JIRA_DOMAIN = os.getenv("JIRA_DOMAIN", "your-domain.atlassian.net")
    PROJECT_KEY = os.getenv("PROJECT_KEY", "YOUR_PROJECT_KEY")
    EPIC_KEY = os.getenv("EPIC_KEY", "YOUR_EPIC_KEY")
    JIRA_EMAIL = os.getenv("JIRA_EMAIL", "your-email@example.com")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "your-jira-api-token")

    # ===== CONFIGURATION GENAI =====
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # ===== CONFIGURATION APPIUM =====
    APPIUM_SERVER = os.getenv("APPIUM_SERVER", "http://localhost:4723")
    APPIUM_PLATFORM = os.getenv("APPIUM_PLATFORM", "Android")
    APPIUM_PLATFORM_VERSION = os.getenv("APPIUM_PLATFORM_VERSION", "16")
    APPIUM_DEVICE_NAME = os.getenv("APPIUM_DEVICE_NAME", "RZCW81HN1XM")
    APPIUM_APP_PACKAGE = os.getenv("APPIUM_APP_PACKAGE", "tn.mobipost")
    APPIUM_APP_ACTIVITY = os.getenv(
        "APPIUM_APP_ACTIVITY",
        "tn.anypli.mobiposte.ui.activity.SplashScreenActivity"
    )

    # ===== CONFIGURATION LOGS =====
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate_jira(cls) -> bool:
        """Valide que toutes les variables Jira sont correctement configurées."""
        missing = []
        
        if not cls.JIRA_DOMAIN or cls.JIRA_DOMAIN == "your-domain.atlassian.net":
            missing.append("JIRA_DOMAIN")
        if not cls.PROJECT_KEY or cls.PROJECT_KEY == "YOUR_PROJECT_KEY":
            missing.append("PROJECT_KEY")
        if not cls.EPIC_KEY or cls.EPIC_KEY == "YOUR_EPIC_KEY":
            missing.append("EPIC_KEY")
        if not cls.JIRA_EMAIL or cls.JIRA_EMAIL == "your-email@example.com":
            missing.append("JIRA_EMAIL")
        if not cls.JIRA_API_TOKEN or cls.JIRA_API_TOKEN == "your-jira-api-token":
            missing.append("JIRA_API_TOKEN")

        if missing:
            print("❌ ERREUR: Configuration Jira incomplète.")
            print("   Variables manquantes ou par défaut :")
            for var in missing:
                print(f"     - {var}")
            print("\n   Action: Remplissez le fichier .env avec vos valeurs réelles.")
            return False
        
        return True

    @classmethod
    def validate_gemini(cls) -> bool:
        """Valide que la clé Gemini est configurée (optionnel mais recommandé)."""
        if not cls.GEMINI_API_KEY:
            print("⚠️ AVERTISSEMENT: GEMINI_API_KEY non configurée.")
            print("   Certains scripts de génération de cas de test ne fonctionneront pas.")
            return False
        return True

    @classmethod
    def validate_appium(cls) -> bool:
        """Valide que la configuration Appium est présente."""
        if not cls.APPIUM_SERVER:
            print("❌ ERREUR: APPIUM_SERVER non configuré.")
            return False
        return True

    @classmethod
    def validate_paths(cls) -> bool:
        """Valide que tous les répertoires de base existent."""
        required_dirs = [cls.TESTING_DIR, cls.REPORT_DIR]
        missing = []
        
        for dir_path in required_dirs:
            if not dir_path.exists():
                missing.append(str(dir_path))
        
        if missing:
            print("❌ ERREUR: Répertoires manquants :")
            for path in missing:
                print(f"     - {path}")
            return False
        
        return True

    @classmethod
    def ensure_output_dirs(cls) -> None:
        """Crée les répertoires de sortie s'ils n'existent pas."""
        output_dirs = [
            cls.SCREENSHOTS_DIR,
            cls.REPORT_JSON_DIR,
            cls.REPORT_PDF_DIR,
            cls.DOCUMENTATION_DIR,
        ]
        
        for dir_path in output_dirs:
            dir_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def print_config(cls, include_secrets: bool = False) -> None:
        """Affiche la configuration actuelle (sans secrets par défaut)."""
        print("\n" + "=" * 70)
        print("CONFIGURATION ACTUELLE")
        print("=" * 70)
        
        print("\n📁 CHEMINS :")
        print(f"  PROJECT_ROOT: {cls.PROJECT_ROOT}")
        print(f"  TESTING_DIR: {cls.TESTING_DIR}")
        print(f"  REPORT_DIR: {cls.REPORT_DIR}")
        
        print("\n🔗 JIRA :")
        print(f"  JIRA_DOMAIN: {cls.JIRA_DOMAIN}")
        print(f"  PROJECT_KEY: {cls.PROJECT_KEY}")
        print(f"  EPIC_KEY: {cls.EPIC_KEY}")
        if include_secrets:
            print(f"  JIRA_EMAIL: {cls.JIRA_EMAIL}")
            print(f"  JIRA_API_TOKEN: {cls.JIRA_API_TOKEN[:10]}..." if cls.JIRA_API_TOKEN else "  JIRA_API_TOKEN: [NOT SET]")
        
        print("\n🤖 APPIUM :")
        print(f"  APPIUM_SERVER: {cls.APPIUM_SERVER}")
        print(f"  APPIUM_PLATFORM: {cls.APPIUM_PLATFORM}")
        print(f"  APPIUM_DEVICE_NAME: {cls.APPIUM_DEVICE_NAME}")
        
        print("\n" + "=" * 70)


def main():
    """Test de la configuration."""
    print("\n🔍 Validating configuration...\n")
    
    jira_ok = Config.validate_jira()
    gemini_ok = Config.validate_gemini()
    appium_ok = Config.validate_appium()
    paths_ok = Config.validate_paths()
    
    Config.ensure_output_dirs()
    Config.print_config()
    
    if jira_ok and paths_ok:
        print("\n✅ Configuration valide !")
        sys.exit(0)
    else:
        print("\n❌ Configuration invalide. Veuillez corriger les erreurs ci-dessus.")
        sys.exit(1)


if __name__ == "__main__":
    main()
