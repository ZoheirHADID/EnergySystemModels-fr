# Script pour traduire automatiquement les fichiers RST du français vers l'anglais
import os
import re

# Dictionnaire de traduction des termes techniques
translation_dict = {
    # Titres et sections
    "Vanne d'équilibrage TA": "TA Balancing Valve",
    "Tour & Andersson": "Tour & Andersson",
    "IMI Hydronic": "IMI Hydronic",
    "Introduction": "Introduction",
    "Types de vannes TA disponibles": "Available TA Valve Types",
    "Guide de paramétrage et exemples d'utilisation": "Configuration Guide and Usage Examples",
    "Applications typiques par type de vanne": "Typical Applications by Valve Type",
    "Résultats des exemples de calcul": "Calculation Examples Results",
    "Nomenclature": "Nomenclature",
    "Équations utilisées": "Equations Used",
    "Données sources et références": "Source Data and References",
    "Tableau récapitulatif des gammes de vannes": "Summary Table of Valve Ranges",
    "Caractéristiques techniques par série": "Technical Characteristics by Series",
    "Conseils d'utilisation et bonnes pratiques": "Usage Tips and Best Practices",
    "Exemples d'erreurs courantes et solutions": "Common Errors and Solutions Examples",
    "Références et documentation complémentaire": "References and Additional Documentation",
    
    # Texte descriptif
    "Les vannes d'équilibrage": "Balancing valves",
    "sont des composants essentiels": "are essential components",
    "dans les systèmes de chauffage, ventilation et climatisation": "in heating, ventilation and air conditioning systems",
    "Elles permettent d'équilibrer hydrauliquement les circuits": "They allow hydraulic balancing of circuits",
    "pour garantir les débits nominaux": "to ensure nominal flow rates",
    "optimiser la performance énergétique": "optimize energy performance",
    "des installations": "of installations",
    
    "Cette classe Python permet de calculer": "This Python class allows calculating",
    "les pertes de charge": "pressure drops",
    "à travers différents modèles de vannes": "through different valve models",
    "en utilisant les": "using the",
    "données Kv officielles": "official Kv data",
    "du fabricant": "from the manufacturer",
    "basées sur le nombre de tours d'ouverture": "based on the number of opening turns",
    
    "L'image ci-dessous montre": "The image below shows",
    "un exemple de": "an example of",
    "vanne d'équilibrage": "balancing valve",
    "installée dans un circuit hydraulique": "installed in a hydraulic circuit",
    
    # Types de vannes
    "Vannes filetées": "Threaded valves",
    "Vannes Venturi": "Venturi valves",
    "Vannes terminales": "Terminal valves",
    "Vannes à brides fonte": "Cast iron flanged valves",
    "Vannes fonte GS": "GS cast iron valves",
    "Vannes grooved Victaulic": "Victaulic grooved valves",
    "Anciennes vannes": "Legacy valves",
    "Orifices fixes de mesure": "Fixed measuring orifices",
    "Régulateurs": "Regulators",
    
    # Applications
    "réseaux secondaires": "secondary networks",
    "réseaux principaux": "main networks",
    "grands réseaux": "large networks",
    "unités terminales": "terminal units",
    "radiateurs": "radiators",
    "ventilo-convecteurs": "fan coil units",
    "équilibrage dynamique": "dynamic balancing",
    "boucles et colonnes": "loops and risers",
    "installations existantes": "existing installations",
    "maintenance": "maintenance",
    
    # Paramètres techniques
    "Nombre de tours": "Number of turns",
    "Diamètre nominal": "Nominal diameter",
    "Perte de charge": "Pressure drop",
    "Débit": "Flow rate",
    "Pression de sortie": "Outlet pressure",
    "Pression d'entrée": "Inlet pressure",
    "Coefficient de débit": "Flow coefficient",
    "Température d'entrée": "Inlet temperature",
    "Densité du fluide": "Fluid density",
    "Débit volumétrique": "Volumetric flow rate",
    "Débit massique": "Mass flow rate",
    "Viscosité dynamique": "Dynamic viscosity",
    
    # Unités
    "tours": "turns",
    "tours d'ouverture": "opening turns",
    
    # Instructions
    "Configuration de la source": "Source configuration",
    "Configuration de la vanne": "Valve configuration",
    "Configuration pour": "Configuration for",
    "Vanne": "Valve",
    "avec": "with",
    "tours": "turns",
    "et un débit de": "and a flow rate of",
    
    # Résultats
    "Paramètre": "Parameter",
    "Valeur": "Value",
    "Type": "Type",
    "Application": "Application",
    "Fonction": "Function",
    
    # Notes et avertissements
    "Le paramètre": "The parameter",
    "peut être spécifié sous forme de": "can be specified as",
    "chaîne de caractères": "string",
    "nombre entier": "integer",
    "la conversion est automatique": "conversion is automatic",
    
    # Documentation
    "Documentation": "Documentation",
    "Références": "References",
    "Normes et standards": "Standards and norms",
    "Outils de calcul complémentaires": "Additional calculation tools",
    "Formation et support": "Training and support",
}

def translate_text(text):
    """Traduit un texte en utilisant le dictionnaire de traduction."""
    for french, english in translation_dict.items():
        # Utiliser une regex pour préserver la casse et la ponctuation
        text = re.sub(re.escape(french), english, text, flags=re.IGNORECASE)
    return text

def translate_file(input_path, output_path):
    """Traduit un fichier RST."""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        translated_content = translate_text(content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"Traduit: {input_path} -> {output_path}")
    except Exception as e:
        print(f"Erreur lors de la traduction de {input_path}: {e}")

def main():
    """Fonction principale pour traduire tous les fichiers RST."""
    base_path_fr = r"A:\OneDrive\_Github_\EnergySystemModels-fr\docs\source"
    base_path_en = r"A:\OneDrive\_Github_\EnergySystemModels-en\docs\source"
    
    # Liste des répertoires à traduire
    directories = [
        "001-heat_transfer",
        "002-thermodynamic_cycles",
        "003-ahu_modules",
        "004-hydraulic",
        "005-aeraulic",
        "010-achat-energie",
        "010-achat-energie/exemples"
    ]
    
    for directory in directories:
        dir_path_fr = os.path.join(base_path_fr, directory)
        dir_path_en = os.path.join(base_path_en, directory)
        
        if os.path.exists(dir_path_fr):
            for filename in os.listdir(dir_path_fr):
                if filename.endswith('.rst'):
                    input_path = os.path.join(dir_path_fr, filename)
                    output_path = os.path.join(dir_path_en, filename)
                    translate_file(input_path, output_path)

if __name__ == "__main__":
    main()
    print("Traduction terminée!")
