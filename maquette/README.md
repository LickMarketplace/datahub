# LICK Datahub — prototype fonctionnel local

L'interface réunit cinq espaces : Accueil, Catalogue, Bibliothèque, Canaux et Règles & contraintes. L'identité LICK reprend le logo original de la présentation fournie et ses couleurs bleu/cyan/turquoise.

Les sources et tests ne contiennent aucun catalogue réel ni document commercial. Le dépôt est public : garder les pièces jointes, sorties préchargées, exports et sauvegardes **hors du dépôt**.

## Générer l'application autonome

Python standard, depuis la racine du dépôt :

```sh
python maquette/build.py --output /tmp/LICK_Datahub_Vierge.html
```

Avec les données privées :

```sh
python maquette/build.py --catalogue /chemin/catalogue.xlsx --boulanger /chemin/BOULANGER.zip --decathlon /chemin/DECATHLON.zip --orange /chemin/ORANGE.zip --output /chemin/prive/LICK_Datahub.html
```

Les paramètres de matrices sont facultatifs. Le générateur intègre le logo, les scripts, le catalogue, les modèles Excel originaux, les métadonnées et les listes de valeurs. Le résultat est un unique HTML autonome. Le fichier source `maquette/index.html` contient des marqueurs et doit passer par ce générateur.

Ouvrir le HTML généré dans Chrome, Edge ou Firefox récent avec IndexedDB et DecompressionStream deflate-raw. Un serveur local peut être utilisé en cas de restriction du navigateur sur les fichiers locaux. Aucun service externe ni dépendance Python à installer. L'application n'a pas d'authentification : ne pas l'exposer publiquement avec des données privées.

## Capacités actuelles

### Accueil et catalogue

Statistiques réelles du dernier import, 13 destinations initiales (lick.fr et 12 marketplaces), contenus validés, documents et erreurs ouvertes. Les indicateurs de complétude vérifient huit champs généraux, sans présumer une conformité marketplace.

Recherche nom/SKU/EAN/marque, pagination, filtres marque/famille/état, images distantes sur activation explicite, consultation des colonnes source, corrections manuelles du titre et de la description avec validation. La provenance peut citer un document, une page et une URL. Les textes et les valeurs de catalogue sont traités comme des données : aucun HTML fournisseur n'est exécuté.

Import réel XLSX/CSV avec feuille, correspondances, aperçu et confirmation. Les changements sont comparés par référence : ajoutés, modifiés et absents. Les absents restent dans les anciennes versions ; les corrections sont conservées séparément et signalées à revoir lorsque leur ligne source change. Un import strictement identique ne crée pas de nouvelle version.

La première ligne non vide contient les en-têtes. Références non vides et uniques requises ; les autres données peuvent être incomplètes. CSV UTF-8/BOM ou Windows-1252, virgule/point-virgule/tabulation et champs cités multilignes. Fichier de 25 Mo et 100 000 articles maximum. XLSX : valeurs enregistrées lues sans exécution des formules ; les formats numériques Excel ne sont pas reconstruits. Enregistrer les EAN et références comme texte pour conserver leurs zéros initiaux.

### Bibliothèque

Dépôt local atomique de notices, fiches techniques, certificats et autres documents PDF/DOCX/XLSX/TXT/JPEG/PNG, 25 Mo par document. Originaux conservés dans IndexedDB, rattachement à plusieurs SKU, marque, langue et type, recherche, téléchargement et retrait. Un nouveau dépôt crée une entrée distincte ; pas de comparaison automatique des versions documentaires.

Liste modifiable des sites de référence HTTPS (fabricants, Icecat, fournisseurs, références spécialisées), marques couvertes et approbation manuelle. Depuis une fiche, des liens de recherche avec EAN s'ouvrent sur action de l'utilisateur et seulement pour les sources approuvées compatibles avec sa marque.

**Aucune extraction documentaire, interrogation automatique de fabricant/Icecat ou IA n'est connectée.** La proposition de description initiale reprend la description du catalogue, ou sa description courte. Les recherches et documents servent à la correction humaine, avec citation et validation finale.

### Canaux et matrices

Destinations initiales : lick.fr, Amazon France (Amazon), Cdiscount (Octopia), Fnac et Darty (portail catalogue commun), Boulanger/Decathlon/Cultura/Castorama/Leroy Merlin/Bricomarché/Orange (Mirakl), ManoMano (Toolbox). De nouveaux canaux peuvent être ajoutés avec leur environnement.

Modèles initiaux intégrés depuis les ZIP Boulanger, Decathlon et Orange. La colonne Orange « Axe de variant » est exclue des catégories. Les variantes d'une même catégorie dans plusieurs modèles restent identifiées par fichier. Les nouveaux modèles et mises à jour s'ajoutent individuellement par XLSX dans l'interface ; l'import ZIP en cours d'utilisation n'est pas implémenté.

Choix explicite d'une famille de catalogue, d'un modèle et d'une catégorie. Correspondances par champ (catalogue, titre/description validés, catégorie ou constante EAN), confirmation des unités et de l'éligibilité de la sélection. **La sélection de catégorie reste manuelle** ; une famille peut être hétérogène et ne doit pas être affectée en bloc sans vérification. Les suggestions de correspondances ne constituent pas un enrichissement fiable par elles-mêmes.

Valeurs spécifiques par SKU/canal/catégorie avec provenance obligatoire pour une valeur ajoutée. Les valeurs peuvent être vidées explicitement ; les obligations continuent de s'appliquer. Les variantes sont filtrées par la catégorie ; le changement de version d'un modèle exige de confirmer de nouveau ses correspondances.

Les contrôles couvrent les attributs obligatoires, les valeurs autorisées de ReferenceData, les limites de longueur configurées, le format connu de description, l'extension JPEG selon règle, les URL d'images, le nombre maximal d'images configuré et la validation du contenu. Les champs NA ne sont pas remplis. Une règle non documentée reste explicitement inconnue ; le format inconnu empêche l'export.

L'export produit un vrai **XLSX basé sur le modèle original**, en remplaçant uniquement les lignes produit de Data. Les deux en-têtes, autres onglets, styles et listes de référence sont conservés. Seuls les articles passant les contrôles sont exportés. Les valeurs sont écrites comme chaînes inline, jamais comme formules. Le diagnostic des articles bloqués est téléchargeable en CSV protégé contre l'injection de formules.

**Un export ne garantit pas l'acceptation par le canal.** Les dimensions/fonds des images, MIME distant, titres dans un ordre grammatical précis, réglementations, contraintes conditionnelles et consignes non structurées doivent encore être vérifiés. Aucune API ni transmission à une marketplace n'est connectée.

### Rapports et règles

Import de rapports CSV/XLSX avec association SKU/EAN/message, conservation des lignes source, rapprochement seulement si le lien est unique et suivi de résolution. Pour une erreur offre Boulanger « The product does not exist », l'action proposée est la création de fiche produit. Les autres messages restent à examiner selon les règles du canal. L'import ne corrige pas automatiquement les sources.

Règles versionnées par destination : longueur titre/modèle/plus produit/accroche/description, format texte/HTML/Markdown, plafond d'images, JPEG et notes sourcées. Les valeurs absentes restent non documentées. Les règles Boulanger/Decathlon et formats Fnac/Darty/Leroy Merlin/Castorama ont une base dans les éléments fournis par l'utilisateur ; les autres doivent être complétées. Les champs spécifiques d'une catégorie restent gouvernés par ses matrices.

## Stockage, sauvegarde et limites

Le stockage est **local au navigateur, au profil et à l'adresse**, sans compte utilisateur, partage, serveur ou synchronisation. Le changement de fichier/origine ou la suppression du stockage peut rendre les données indisponibles. Conserver les originaux et télécharger régulièrement une sauvegarde.

La sauvegarde complète JSON inclut versions, validations et citations, documents originaux, sites, règles, correspondances, modèles, listes de valeurs et rapports. Restauration atomique dans un espace vide ; 250 Mo maximum par sauvegarde restaurée. L'ancien format `lick-datahub-reconstruction` schema 1 est accepté ; les modifications de prototypes plus anciens non sauvegardées ne sont pas récupérées. Une restauration peut nécessiter une version vierge de l'application et un autre profil de navigateur.

Aucun document réel, fichier catalogue ou matrice n'est ajouté au dépôt Git. Les fichiers autonomes préchargés sont privés. Les images externes et recherches consultent des sites tiers uniquement après activation/action explicite.

## Validation

`node tests/hub-browser.cjs /chemin/prive/LICK_Datahub.html /chemin/prive/resultats` avec Playwright et Chromium. `CHROMIUM_PATH` peut choisir le navigateur. Le contrôle utilise les pièces de référence de cette conversation (2 720 articles et 113 matrices) et des données synthétiques pour les écritures/export ; aucune fixture commerciale n'est incluse dans les sources.

Vérifications : accueil, catalogue, persistance des corrections, bibliothèque et octets des documents, sites, règles versionnées, catégories Orange sans axe de variant, rapport et suivi, export XLSX, blocage hors liste, sauvegarde/restauration complète, mobile et erreurs JavaScript. Les fichiers exportés peuvent ensuite être relus avec `zipfile`/XML pour contrôler le ZIP, les cellules et les onglets conservés.

## Démonstration sans données commerciales

`python maquette/build.py --demo --output /tmp/LICK_Datahub_Maquette.html` génère une version navigable avec six articles et trois modèles entièrement fictifs. L'interface les identifie comme tels et bloque leurs exports. La démonstration utilise un stockage de navigateur séparé (`lick-datahub-demo-v1`) pour préserver celui du prototype réel. L'archive prête à ouvrir se trouve dans `demo/`. Test : `node tests/demo-browser.cjs /tmp/LICK_Datahub_Maquette.html` avec Playwright et Chromium disponibles.
