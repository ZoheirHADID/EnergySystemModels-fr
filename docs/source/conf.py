# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'EnergySystemModels'
# Annee courante incluse : le pied de page de chaque page affiche cette ligne.
copyright = '2024-2026, Zoheir HADID'
author = 'Zoheir HADID'

release = 'post9'
version = '0.1.23'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
# Menu latéral : titres de pages seulement, sans leurs sous-sections
# (« Utilisation », « Paramètres »…) — demande de l'utilisateur, 2026-09-28.
html_theme_options = {'titles_only': True}

# Largeur : le thème limite le contenu à 800 px, ce qui laissait la moitié de
# l'écran vide et serrait les tableaux à cinq colonnes. La feuille ci-dessous
# lève cette limite (demande de Zoheir, 2026-11-26).
html_css_files = ['esm_pleine_largeur.css']
html_static_path = ['_static']

# -- Options for EPUB output
epub_show_urls = 'footnote'
