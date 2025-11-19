# Corrections apportées à TA_valve.rst
# =====================================

## Problèmes identifiés dans le fichier original :

1. **Contenu dupliqué et mélangé** : Le fichier contenait du contenu en français et en anglais mélangé de manière incohérente
2. **Tableaux corrompus** : Les tableaux RST étaient mal formatés avec du code Python inséré au milieu
3. **Exemples incorrects** : Les exemples utilisaient DN65 au lieu de STAF-DN100 comme dans test_TA.py
4. **Valeurs incorrectes** : Les valeurs de résultats ne correspondaient pas aux calculs réels

## Corrections effectuées :

### 1. Nettoyage de la structure
- Supprimé toutes les duplications de titre
- Unifié le contenu en français uniquement
- Restructuré les sections de manière logique

### 2. Correction de l'exemple principal
**Avant :**
```python
SOURCE.Pi_bar = 1.01325      # 1.01325 bar
SOURCE.F_m3h = 27            # 27 m³/h
vanne.dn = "DN65"
vanne.nb_tours = 5.0
```

**Après (conforme à test_TA.py) :**
```python
SOURCE.Pi_bar = 3.0          # 3 bar
SOURCE.F_m3h = 70            # 70 m³/h
vanne.dn = "STAF-DN100"
vanne.nb_tours = 4.3
```

### 3. Correction des valeurs calculées
**Pour STAF-DN100 avec 4.3 tours et 70 m³/h :**
- Kv interpolé : ~81.4 m³/h (au lieu de 52 m³/h)
  - Calcul : Kv(4.3) = 66 + (91.7-66) × (4.3-4)/(4.5-4) = 81.4
- Perte de charge : ~73500 Pa (~0.74 bar)
  - Calcul : ΔP = (70/81.4)² × 10⁵ = 73960 Pa
- Pression sortie : ~2.26 bar (au lieu de 0.74 bar)
  - Calcul : P_out = 3.0 - 0.74 = 2.26 bar

### 4. Ajout d'informations manquantes
- Ajouté la mention "120+ références" au lieu de "50+"
- Ajouté MDFO dans le tableau récapitulatif
- Précisé l'usage de nb_tours = 0 pour régulateurs et orifices fixes
- Ajouté des exemples d'interpolation cohérents

### 5. Correction de la nomenclature
- Vérifié que tous les paramètres correspondent au code source (TA_Valve.py)
- Supprimé la référence à "Kv" comme attribut direct (non stocké dans la classe)
- Unifié "delta_P" partout

## Fichiers de référence utilisés :
1. `test_TA.py` : Pour l'exemple principal et les valeurs
2. `TA_Valve.py` : Pour les paramètres de classe et la logique de calcul
3. Documentation IMI TA : Pour les valeurs Kv tabulées

## Résultat :
✓ Fichier RST cohérent et utilisable
✓ Exemples fonctionnels alignés avec le code de test
✓ Valeurs calculées correctes
✓ Structure claire et professionnelle
✓ Sauvegarde créée : TA_valve.rst.backup
