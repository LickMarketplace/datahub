# Accès de test privé Lick Datahub

Ce composant prépare un accès HTTP protégé au prototype autonome existant. **Il ne publie pas de site et ne crée pas d'URL publique.** Un hébergement Node.js et une adresse HTTPS restent nécessaires pour un accès depuis un autre ordinateur.

Node.js 22 ou supérieur, bibliothèque standard uniquement. Le catalogue n'est pas inclus dans ces sources et ne doit pas être publié dans le dépôt GitHub public.

Variables à configurer dans les paramètres sécurisés de l'hébergement :

- `DATAHUB_HTML_PATH` : chemin vers le HTML autonome privé, sur le serveur.
- `DATAHUB_PREVIEW_USER` : identifiant de l'accès, `lick` par défaut.
- `DATAHUB_PREVIEW_PASSWORD` : mot de passe d'au moins 16 caractères ; ne pas le partager dans le chat ni le committer.
- `DATAHUB_BIND_HOST` : `127.0.0.1` par défaut ; `0.0.0.0` pour un hébergement qui l'exige.
- `PORT` : port fourni par l'hébergement, 8080 par défaut.

Commande : `node preview/server.cjs` depuis la racine du dépôt.

Le serveur expose uniquement le HTML authentifié et un contrôle de santé `/healthz` sans donnée métier. Les requêtes POST et l'accès aux autres fichiers sont refusés. L'hébergement doit terminer TLS pour une URL HTTPS ; l'authentification HTTP Basic ne doit pas être utilisée sur un accès Internet HTTP non chiffré. Ne pas rendre le HTML accessible par un service de fichiers statiques qui contournerait cette protection.

Le prototype conserve toujours les imports, documents et corrections **dans le navigateur de l'utilisateur**, sans base serveur ni synchronisation. Ce mode permet d'évaluer l'interface pour un seul utilisateur ; il ne fournit pas encore d'authentification applicative multiutilisateur ou de stockage collaboratif. Les recherches Google et images externes restent déclenchées par action utilisateur.

Les sources n'incluent aucune clé d'hébergement. Avant tout déploiement, choisir une destination autorisée, y configurer l'accès et transférer le HTML privé via un moyen sécurisé pris en charge par cet hébergement. La taille du fichier préchargé dépasse les limites de réponse de certaines offres serverless ; privilégier un service Node capable de servir des réponses en streaming plutôt qu'une fonction limitée à quelques mégaoctets.

Contrôle local : `node tests/preview-server.cjs`. Un démarrage réussi dans l'environnement Codex ne crée pas une URL consultable par l'utilisateur du chat.

## Proposition Render

`render.yaml` et `preview/Dockerfile` préparent un service de test Render. Ces fichiers ne créent rien tant que le code n'est pas disponible dans un dépôt autorisé et que le déploiement n'est pas lancé depuis un compte Render.

Le Dockerfile construit une interface **vierge** à partir des seules sources. Aucun catalogue, matrice, document ou mot de passe n'est inclus dans le dépôt ou l'image. Le mot de passe d'accès est généré par l'hébergeur ; il se consulte dans les paramètres sécurisés du service. Vérifier l'offre disponible et ses conditions dans l'interface de l'hébergeur avant de confirmer. Le fichier propose une offre gratuite, sans garantir sa disponibilité ni ses limites de mise en veille.

Le compte de test accède au site avec l'identifiant `lick` et ce mot de passe. Les modifications ne sont pas redéployées automatiquement. Pour préparer les données après connexion : importer le catalogue Excel, extraire les archives de matrices sur son ordinateur, puis sélectionner les fichiers XLSX de chaque enseigne dans Canaux. Le navigateur conserve ces données localement ; le serveur ne les reçoit pas.

Deux autorisations externes restent nécessaires : enregistrer le code sans données commerciales dans le dépôt choisi, puis lancer le déploiement depuis le compte d'hébergement. Ne jamais publier le HTML préchargé de `/workspace/private-datahub` dans le dépôt public.
