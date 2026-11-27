# -*- coding: utf-8 -*-
"""Valeurs **démontrées** des paramètres d'une fiche CEE.

Une valeur n'est publiée comme « possible » que si elle est **exécutée par la
page** : les exemples de référence du tableau de synthèse passent ces valeurs à
``calcul_CEE``, le banc compare la sortie publiée à la sortie réelle, et une
valeur refusée ferait tomber la page. C'est donc une valeur que le code
**accepte**, prouvée à chaque construction du guide.

Trois formes de valeurs, distinguées dans le tableau :

* ``'pompage'`` — une valeur **littérale** démontrée (choix de la fiche) ;
* ``111 ≤ etas`` — une **contrainte numérique** lue dans la docstring de la
  fiche (bornes, tranches), qui dit ce qui est admis sans prétendre à une liste ;
* ``ex. 110`` — la seule **valeur de test** démontrée, quand rien d'autre n'est
  cité. Le tableau écrit alors « valeur testée », jamais « valeurs admises ».

Ce que ce module ne fait pas, et ne prétend pas faire : reconstituer la liste
complète des valeurs admises d'une fiche. Mesure du 2026-11-26 : les docstrings
citent des valeurs pour 26 % des paramètres seulement (et aucune pour 112 des
214 fiches), les messages d'erreur n'énumèrent les choix que 8 fois sur 115.
Fabriquer une liste pour le reste serait de l'invention ; le tableau le dit.
"""

from __future__ import annotations

import re

#: Contraintes chiffrées qu'une docstring énonce : « P (kW) <= 3000 »,
#: « Etas >= 111 % », « 2 <= N < 10 », « 111-140 ».
_CONTRAINTE = re.compile(r"(<=|>=|≤|≥|<|>)\s*(\d[\d\s.,]*)")


#: Paramètres géographiques et **domaine** publié par le modèle CEE : les trois
#: zones climatiques (``CEE.H1``, ``CEE.H2``, ``CEE.H3``) et les départements de
#: ces listes. Ce n'est pas une valeur de test : c'est l'ensemble des valeurs que
#: la bibliothèque reconnaît (``if zone == "H1"`` …). Le tableau le publie même
#: quand l'appel de référence ne passe que l'un des trois.
ZONES_GEOGRAPHIQUES = {
    "zone": '``"H1"``, ``"H2"``, ``"H3"``',
    "zone_geographique": '``"H1"``, ``"H2"``, ``"H3"``',
    "departement": "numéro (69) ou code (``\"2A\"``) — cf. ``CEE.H1/H2/H3``",
    "Department": "numéro (69) ou code (``\"2A\"``) — cf. ``CEE.H1/H2/H3``",
}


def contraintes(doc: str, parametre: str = "", limite: int = 2) -> list[str]:
    """Bornes et tranches que la docstring énonce **pour ce paramètre**.

    On lit la phrase qui suit le nom du paramètre (jusqu'au point) : les bornes
    trouvées ailleurs dans la docstring concernent d'autres grandeurs et n'ont
    rien à faire dans la cellule de celle-ci. Ce comportement a été corrigé le
    2026-11-26 : la première version collait à tous les paramètres les bornes de
    la fiche (« >= 160 ; < 35 » sur une zone climatique).
    """
    if not doc or not parametre:
        return []
    phrase = ""
    for trouve in re.finditer(r"`?%s`?" % re.escape(parametre), doc):
        suite = doc[trouve.end():]
        fin = re.search(r"[.;]\s|\n\s*\n", suite)
        candidate = suite[:fin.start()] if fin else suite
        if _CONTRAINTE.search(candidate):
            phrase = candidate
            break
    vues: list[str] = []
    for op, nombre in _CONTRAINTE.findall(phrase):
        fragment = "%s %s" % (op.strip(), nombre.strip().rstrip(".,;"))
        if fragment not in vues:
            vues.append(fragment)
        if len(vues) >= limite:
            break
    return vues


def litteral(valeur: str) -> str:
    """Vrai si la valeur de test est un littéral Python (chaîne entre guillemets)."""
    valeur = (valeur or "").strip()
    return len(valeur) >= 2 and valeur[0] == valeur[-1] and valeur[0] in "'\""


def cellule(valeur: str, contraintes_parametre: list[str] | None = None) -> str:
    """Texte de la cellule « valeur possible » d'un paramètre.

    * littéral démontré → ``'pompage'`` (la valeur que le code accepte) ;
    * contraintes du paramètre → les bornes que la docstring énonce pour lui ;
    * sinon → ``ex. 90`` et la mention « valeur testée », qui ne prétend pas
      être une liste.
    """
    valeur = (valeur or "").strip()
    if litteral(valeur):
        return "``%s``" % valeur.replace('"', "'")
    bornes = contraintes_parametre or []
    if bornes:
        return "ex. %s (%s)" % (valeur, " ; ".join(bornes))
    return "ex. %s" % (valeur or "—")
