.. _utilisation:

Utilisation
===========

Pour utiliser les modules AHU, vous devez les intégrer dans votre système de gestion de bâtiment. Les modules peuvent être configurés et contrôlés via l'API fournie.

Exemple
-------

Voici un exemple de la façon d'initialiser et de configurer un module AHU :

.. code-block:: python

    from ahu_module import AHU

    ahu = AHU()
    ahu.set_temperature(22)  # Régler la température à 22 degrés Celsius
    ahu.set_humidity(50)     # Régler l'humidité à 50%
    ahu.start()