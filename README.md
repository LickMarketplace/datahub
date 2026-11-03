# Lick Datahub

Socle de démarrage du futur outil d'enrichissement des données produits.

## Environnement Codex
Python 3.11 ou supérieur. Aucune dépendance externe à installer à ce stade.
Exécuter les commandes depuis la racine du dépôt.

Commande de préparation :
```sh
python --version
python -m compileall -q datahub
```

Commande de validation :
```sh
python -m datahub check
```

Inspection de la structure d'un catalogue (sans afficher ses valeurs) :
```sh
python -m datahub inspect-csv /chemin/catalogue.csv --delimiter ";"
```
Encodage par défaut : UTF-8 avec ou sans BOM. Utiliser --encoding cp1252 si nécessaire.
Le contrôle signale les en-têtes vides/dupliqués et les lignes dont la largeur diffère.
Il ne valide pas encore les EAN ni les règles des marketplaces.

## Stockage prévu
- GitHub : code, configuration sans secrets et documentation.
- PostgreSQL / Supabase : produits, attributs, provenance, règles et historique.
- Supabase Storage privé : catalogues, matrices, notices, rapports et exports.

Aucun service cloud ni stockage persistant n'est provisionné par ce dépôt.
La commande check vérifie uniquement le démarrage local, pas une connexion Supabase.
Un prototype local avec import Excel/CSV, bibliothèque, règles et exports de matrices est disponible dans `maquette/`. L'enrichissement automatique et les API restent à connecter.

## Confidentialité
Ce dépôt est public. Ne pas y ajouter de catalogue réel, document commercial ou secret.
Les dossiers data/ et exports/ et les fichiers .env sont ignorés par Git.
Prévoir des sauvegardes distinctes de la base et des fichiers avant la production.

## Prochain jalon
Connecter le stockage privé puis traiter une matrice, une catégorie et un échantillon
de produits avec conservation de la source de chaque caractéristique.

## Prototype Datahub

Voir [la documentation du prototype](maquette/README.md) : Accueil, Catalogue, Bibliothèque, Canaux, Règles & contraintes. Les données restent dans le navigateur et les sorties préchargées doivent être conservées hors de ce dépôt public.

```sh
python maquette/build.py --output /tmp/LICK_Datahub_Vierge.html
```
