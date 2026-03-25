# Manuel utilisateur

**OpenRAG Playground** est une interface de démonstration pour [Open-RAG](https://open-rag.ai), la plateforme souveraine de Génération Augmentée par Recherche de [LINAGORA](https://linagora.com). Elle permet aux opérateurs de réaliser des démos en direct via des connexions par persona, chacune adossée à un vrai token API OpenRAG.

## Prise en main

### Premier lancement

Lors du premier lancement d'OpenRAG Playground, un assistant de configuration s'affiche. Il vous guide en cinq étapes :

1. **Mot de passe principal** -- Choisissez un mot de passe robuste. Ce mot de passe protège tous les accès à l'application et sert à chiffrer les tokens API. Il ne peut pas être récupéré en cas de perte ; le seul mécanisme de réinitialisation est de supprimer le fichier de configuration.
2. **Groupes** -- Définissez des groupes pour organiser les utilisateurs de démo (ex : départements, équipes). Chaque groupe possède un nom, une couleur et une icône Lucide.
3. **Utilisateurs de démo** -- Créez des comptes persona. Chaque utilisateur nécessite un nom, un titre de poste, un groupe, un style d'avatar (masculin/féminin/neutre), une couleur d'avatar, une URL d'API OpenRAG et un vrai token API.
4. **Prompts de démo** -- Pré-configurez des prompts accessibles rapidement avec le raccourci `/`. Chaque prompt possède un libellé, une portée (globale, spécifique à un groupe ou à un utilisateur), des tags optionnels et le texte du prompt.
5. **Vérification et confirmation** -- Relisez tous les paramètres et créez la configuration.

La configuration est enregistrée dans `config.yaml`. Les tokens sont chiffrés en AES-256-GCM avec une clé dérivée du mot de passe principal.

### Déverrouillage de l'application

Chaque visite nécessite la saisie du mot de passe principal. Une fois saisi, une session de 24 heures est créée. Toutes les pages sont protégées derrière cette porte d'entrée.

## Page de connexion

Après le déverrouillage, la page de connexion affiche une grille de cartes persona organisées par groupe. Chaque carte montre l'avatar, le nom, le titre de poste et le badge de groupe de l'utilisateur.

- **Simple clic** sur une carte pour ouvrir la fenêtre de connexion. Celle-ci affiche un champ de mot de passe décoratif pré-rempli et un bouton "Se connecter".
- **Double-clic** sur une carte pour masquer cet utilisateur de la grille pour la session en cours. Utile lors des démos pour n'afficher que les personas pertinentes.
- Appuyez sur **Échap** pour fermer la fenêtre de connexion.

## Interface de chat

### Disposition

L'interface de chat comporte deux zones principales :

- **Barre latérale** (gauche) -- Contient l'arborescence des partitions, le navigateur de fichiers et l'historique des messages.
- **Zone de chat** (droite) -- Contient l'en-tête du chat, le flux de messages et la barre de saisie.

### Envoi de messages

Tapez votre message dans la barre de saisie en bas et appuyez sur **Entrée** pour envoyer. Les réponses sont diffusées en temps réel via Server-Sent Events -- les tokens apparaissent un par un au fur et à mesure de leur génération.

Les réponses sont rendues avec un support complet du markdown : titres, gras, italique, blocs de code, listes et tableaux sont tous formatés.

### Sources

Après chaque réponse, le système affiche les documents sources utilisés pour générer la réponse. Chaque source montre le nom du fichier, un score de pertinence et un extrait. Cliquez sur une source pour ouvrir le visualiseur, qui prend en charge :

- Documents PDF (visualiseur intégré)
- Images (affichage en ligne)
- Fichiers audio (lecteur audio)
- Fichiers vidéo (lecteur vidéo)
- Fichiers texte et markdown (contenu rendu)
- Autres types de fichiers (lien de téléchargement)

### Effacer la conversation

Cliquez sur l'icône gomme dans le coin supérieur gauche de la zone de chat pour effacer la conversation en cours.

## Recherche sémantique

Préfixez votre message par `#` pour effectuer une recherche sémantique au lieu d'une requête de chat. Par exemple :

```
# clauses de résiliation de contrat de travail
```

Cela retourne les fragments de documents les plus pertinents de la partition active sans générer de réponse IA. Les résultats s'affichent sous forme de cartes sources cliquables.

## Suggestions de prompts

Tapez `/` dans la barre de saisie pour ouvrir le menu déroulant des suggestions de prompts. Celui-ci affiche tous les prompts de démo pré-configurés disponibles pour l'utilisateur actuel en fonction de la portée (global, groupe, utilisateur ou partition). Utilisez les flèches **Haut/Bas** pour naviguer et **Entrée** pour sélectionner un prompt.

Les prompts peuvent aussi être sauvegardés depuis l'historique : survolez un message dans la barre latérale d'historique et cliquez sur l'icône de signet pour l'enregistrer comme prompt de démo avec la portée choisie (pour tout le monde, pour mon groupe, pour cette partition ou pour moi uniquement).

## Arborescence des partitions

La barre latérale affiche toutes les partitions disponibles sous forme d'arborescence de dossiers. Les partitions sont des espaces de données qui organisent les documents par sujet ou département.

- **all** est toujours listé en premier et agrège toutes les partitions.
- Cliquez sur une partition pour la sélectionner. Le chat et le navigateur de fichiers refléteront la partition sélectionnée.
- Cliquez sur la flèche à côté d'une partition pour la déplier et voir ses fichiers et fragments.
- Les fichiers s'affichent en arborescence sous chaque partition. Cliquez sur un fichier pour le visualiser. Cliquez sur la flèche à côté d'un fichier pour voir ses fragments indexés.
- Chaque partition affiche un badge de rôle (propriétaire, éditeur ou lecteur) indiquant votre niveau d'accès.

### Navigation dans les fichiers et fragments

Lorsqu'une partition est dépliée, ses fichiers apparaissent en sous-arborescence. Chaque fichier affiche son nom et une icône de type. Déplier un fichier révèle les fragments individuels qui en ont été indexés.

- Cliquez sur le nom d'un fichier pour l'ouvrir dans le visualiseur.
- Cliquez sur un fragment pour voir le contenu de ce fragment spécifique.
- Survolez un fichier pour faire apparaître les boutons d'action : visualiser, ouvrir dans un nouvel onglet et supprimer (si vous avez un accès éditeur ou propriétaire).

## Envoi de fichiers

Si vous disposez d'un accès éditeur ou propriétaire sur une partition, un bouton d'envoi apparaît dans l'en-tête de la barre latérale. Cliquez dessus pour sélectionner un fichier à envoyer. Les types de fichiers pris en charge dépendent de la configuration du serveur OpenRAG.

Après l'envoi, le fichier est mis en file d'attente pour indexation. L'interface interroge l'état de la tâche et met à jour l'affichage lorsque l'indexation est terminée.

## Gestion des accès aux partitions

Pour les partitions dont vous êtes propriétaire, survolez le nom de la partition et cliquez sur l'icône de bouclier pour gérer les accès. Un panneau s'ouvre affichant tous les utilisateurs ayant accès à la partition et leurs rôles. Les propriétaires peuvent modifier les rôles des utilisateurs pour cette partition.

## Panneau d'administration

Le panneau d'administration est accessible à l'adresse `/admin` (non lié dans la navigation principale). Il nécessite la même session maître que l'application principale.

Le panneau d'administration propose quatre sections accessibles via des onglets :

- **Groupes** -- Ajouter, modifier ou supprimer des groupes. Chaque groupe possède un nom, une couleur et une icône.
- **Utilisateurs de démo** -- Ajouter, modifier ou supprimer des personas. Vous pouvez utiliser le bouton "Récupérer les infos utilisateur" pour remplir automatiquement les détails depuis l'API. Le changement de mot de passe principal re-chiffre tous les tokens.
- **Prompts de démo** -- Ajouter, modifier ou supprimer des prompts pré-configurés avec libellés, portées, tags et texte.
- **Paramètres** -- Exporter et importer des fichiers de configuration.

Le panneau d'administration propose aussi un bouton de déconnexion pour terminer la session maître et revenir à l'écran de déverrouillage.

## Menu utilisateur

Cliquez sur votre avatar et votre nom dans le coin supérieur droit de l'en-tête du chat pour ouvrir le menu utilisateur. Depuis celui-ci, vous pouvez :

- **Changer de langue** entre l'anglais et le français.
- **Changer de thème** entre le mode sombre et le mode clair.
- **Accéder à l'administration** (ouvre `/admin`).
- **Se déconnecter** pour revenir à l'écran de sélection de persona.

## Raccourcis clavier

| Raccourci | Action |
|---|---|
| Entrée | Envoyer le message |
| Échap | Fermer la fenêtre modale, fermer la fenêtre de connexion, fermer le visualiseur |
| Haut / Bas | Naviguer dans les suggestions de prompts |
| / | Ouvrir les suggestions de prompts (quand la saisie est vide) |
| # | Lancer une recherche sémantique (quand la saisie est vide) |
