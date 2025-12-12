import json
from pylatex import Document, Section, Subsection, Itemize, Enumerate
from pylatex.utils import bold

# Charger le JSON
with open(r"C:\Users\MSI\D17Testing\Testing\report_json\rapport_connexion_d17.json", "r", encoding="utf-8") as f:
    tests = json.load(f)

# Créer le document LaTeX
doc = Document()
doc.preamble.append(r'\usepackage[french]{babel}')
doc.preamble.append(r'\usepackage[utf8]{inputenc}')
doc.preamble.append(r'\usepackage[a4paper,margin=2cm]{geometry}')

# Titre et Table des matières
doc.preamble.append(r'\title{Rapport des Tests Automatisés}')
doc.preamble.append(r'\date{\today}')
doc.append(r'\maketitle')
doc.append(r'\tableofcontents')
doc.append(r'\newpage')

# Ajouter chaque test
for test in tests:
    with doc.create(Section(f"{test['ID_Test']} - {test['Titre_Test']}")):
        # Infos principales
        doc.append(f"{bold('Données Test:')} {test['Données_Test']}\n\n")
        doc.append(f"{bold('Résultat Attendu:')} {test['Résultat_Attendu']}\n\n")
        doc.append(f"{bold('Statut d\'Exécution:')} {test['Statut_Execution']}\n\n")
        doc.append(f"{bold('Date d\'Exécution:')} {test['Date_Execution']}\n\n")
        doc.append(f"{bold('Note défaut:')} {test['Note_Defaut']}\n\n")
        
        # Étapes du test
        doc.append(f"{bold('Étapes Test:')}\n")
        with doc.create(Enumerate()) as enum:
            for step in test['Étapes_Test']:
                enum.add_item(step)

# Générer le fichier .tex et le PDF si LaTeX est installé
doc.generate_tex("tests_report")       # Génère tests_report.tex
# doc.generate_pdf("tests_report", clean_tex=False)  # Décommenter si LaTeX installé

print("Fichier LaTeX généré : tests_report.tex")
