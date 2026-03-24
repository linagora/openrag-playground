# Copyright 2026 LINAGORA
# SPDX-License-Identifier: AGPL-3.0-only
"""Translations EN/FR, t() helper, language detection."""

from flask import Flask, request, session

TRANSLATIONS = {
    "unlock.title": {
        "en": "OpenRAG Playground",
        "fr": "OpenRAG Playground",
    },
    "unlock.subtitle": {
        "en": "Enter the master password to continue",
        "fr": "Entrez le mot de passe principal pour continuer",
    },
    "unlock.placeholder": {
        "en": "Master password",
        "fr": "Mot de passe principal",
    },
    "unlock.button": {
        "en": "Unlock",
        "fr": "Déverrouiller",
    },
    "unlock.error": {
        "en": "Invalid password",
        "fr": "Mot de passe invalide",
    },
    "footer.about": {
        "en": "About",
        "fr": "À propos",
    },
    "footer.gdpr": {
        "en": "GDPR",
        "fr": "RGPD",
    },
    "footer.ai_act": {
        "en": "AI Act",
        "fr": "AI Act",
    },
    "footer.sovereignty": {
        "en": "Data Sovereignty",
        "fr": "Souveraineté des données",
    },
    "footer.legal": {
        "en": "Legal Notice",
        "fr": "Mentions légales",
    },

    # Setup wizard
    "setup.title": {
        "en": "Initial Setup",
        "fr": "Configuration initiale",
    },
    "setup.subtitle": {
        "en": "Configure your OpenRAG Playground in a few steps",
        "fr": "Configurez votre OpenRAG Playground en quelques étapes",
    },
    "setup.next": {
        "en": "Next",
        "fr": "Suivant",
    },
    "setup.back": {
        "en": "Back",
        "fr": "Retour",
    },
    "setup.step_of": {
        "en": "Step {n} of {total}",
        "fr": "Étape {n} sur {total}",
    },

    # Step 1
    "setup.step1.title": {
        "en": "Master Password",
        "fr": "Mot de passe principal",
    },
    "setup.step1.password": {
        "en": "Password",
        "fr": "Mot de passe",
    },
    "setup.step1.confirm": {
        "en": "Confirm password",
        "fr": "Confirmer le mot de passe",
    },

    # Step 2
    "setup.step2.title": {
        "en": "Groups",
        "fr": "Groupes",
    },
    "setup.step2.desc": {
        "en": "Define groups to organize your demo users (e.g. departments, teams).",
        "fr": "Définissez des groupes pour organiser vos utilisateurs de démo (ex: départements, équipes).",
    },
    "setup.step2.label": {
        "en": "Name",
        "fr": "Nom",
    },
    "setup.step2.color": {
        "en": "Color",
        "fr": "Couleur",
    },
    "setup.step2.icon": {
        "en": "Icon",
        "fr": "Icône",
    },
    "setup.step2.empty": {
        "en": "No groups yet. Add one above.",
        "fr": "Aucun groupe. Ajoutez-en un ci-dessus.",
    },

    # Step 3
    "setup.step3.title": {
        "en": "Demo Users",
        "fr": "Utilisateurs de démo",
    },
    "setup.step3.desc": {
        "en": "Each user has a real OpenRAG API token. Tokens will be encrypted with your master password.",
        "fr": "Chaque utilisateur dispose d'un vrai token API OpenRAG. Les tokens seront chiffrés avec votre mot de passe principal.",
    },
    "setup.step3.name": {
        "en": "Full name",
        "fr": "Nom complet",
    },
    "setup.step3.job_title": {
        "en": "Job title",
        "fr": "Fonction",
    },
    "setup.step3.group": {
        "en": "Group",
        "fr": "Groupe",
    },
    "setup.step3.genre": {
        "en": "Genre",
        "fr": "Genre",
    },
    "setup.step3.avatar_color": {
        "en": "Color",
        "fr": "Couleur",
    },
    "setup.step3.api_url": {
        "en": "API URL",
        "fr": "URL de l'API",
    },
    "setup.step3.token": {
        "en": "API Token (plaintext)",
        "fr": "Token API (en clair)",
    },
    "setup.step3.add": {
        "en": "Add user",
        "fr": "Ajouter l'utilisateur",
    },
    "setup.step3.empty": {
        "en": "No users yet. Add one above.",
        "fr": "Aucun utilisateur. Ajoutez-en un ci-dessus.",
    },

    # Step 4
    "setup.step4.title": {
        "en": "Demo Prompts",
        "fr": "Prompts de démo",
    },
    "setup.step4.desc": {
        "en": "Pre-configured prompts users can pick from with the / shortcut.",
        "fr": "Prompts pré-configurés que les utilisateurs peuvent sélectionner avec le raccourci /.",
    },
    "setup.step4.label": {
        "en": "Label",
        "fr": "Libellé",
    },
    "setup.step4.scope": {
        "en": "Scope",
        "fr": "Portée",
    },
    "setup.step4.tags": {
        "en": "Tags (comma-separated)",
        "fr": "Tags (séparés par des virgules)",
    },
    "setup.step4.prompt": {
        "en": "Prompt text",
        "fr": "Texte du prompt",
    },
    "setup.step4.add": {
        "en": "Add prompt",
        "fr": "Ajouter le prompt",
    },
    "setup.step4.empty": {
        "en": "No prompts yet. Add one above.",
        "fr": "Aucun prompt. Ajoutez-en un ci-dessus.",
    },

    # Step 5
    "setup.step5.title": {
        "en": "Review & Confirm",
        "fr": "Vérification & Confirmation",
    },
    "setup.step5.password_set": {
        "en": "Master password configured",
        "fr": "Mot de passe principal configuré",
    },
    "setup.step5.groups": {
        "en": "Groups",
        "fr": "Groupes",
    },
    "setup.step5.users": {
        "en": "Demo Users",
        "fr": "Utilisateurs de démo",
    },
    "setup.step5.prompts": {
        "en": "Demo Prompts",
        "fr": "Prompts de démo",
    },
    "setup.step5.none": {
        "en": "None configured",
        "fr": "Aucun configuré",
    },
    "setup.step5.confirm": {
        "en": "Create configuration",
        "fr": "Créer la configuration",
    },
    "setup.create": {
        "en": "Create & Continue",
        "fr": "Créer & Continuer",
    },

    # Admin
    "admin.title": {
        "en": "Administration",
        "fr": "Administration",
    },
    "admin.subtitle": {
        "en": "Manage groups, users, and prompts",
        "fr": "Gérer les groupes, utilisateurs et prompts",
    },
    "admin.back_to_app": {
        "en": "Back to application",
        "fr": "Retour à l'application",
    },
    "admin.logout": {
        "en": "Logout",
        "fr": "Déconnexion",
    },
    "admin.logout_tooltip": {
        "en": "Disconnect from master session",
        "fr": "Se déconnecter de la session maître",
    },
    "admin.export": {
        "en": "Export config",
        "fr": "Exporter la config",
    },
    "admin.export_tooltip": {
        "en": "Download config.yaml with decrypted tokens",
        "fr": "Télécharger config.yaml avec les tokens en clair",
    },
    "admin.import": {
        "en": "Import config",
        "fr": "Importer une config",
    },
    "admin.import_tooltip": {
        "en": "Upload a config.yaml file (tokens will be encrypted)",
        "fr": "Importer un fichier config.yaml (les tokens seront chiffrés)",
    },
    "admin.save": {
        "en": "Save",
        "fr": "Enregistrer",
    },
    "admin.cancel": {
        "en": "Cancel",
        "fr": "Annuler",
    },
    "admin.user.token_leave_empty": {
        "en": "leave empty to keep current",
        "fr": "laisser vide pour conserver l'actuel",
    },
    "admin.confirm_delete": {
        "en": "Delete this item?",
        "fr": "Supprimer cet élément ?",
    },

    # Admin — Groups
    "admin.groups": {
        "en": "Groups",
        "fr": "Groupes",
    },
    "admin.group.label": {
        "en": "Name",
        "fr": "Nom",
    },
    "admin.group.color": {
        "en": "Color",
        "fr": "Couleur",
    },
    "admin.group.icon": {
        "en": "Icon",
        "fr": "Icône",
    },
    "admin.group.empty": {
        "en": "No groups yet. Add one above.",
        "fr": "Aucun groupe. Ajoutez-en un ci-dessus.",
    },

    # Admin — Users
    "admin.users": {
        "en": "Demo Users",
        "fr": "Utilisateurs de démo",
    },
    "admin.user.name": {
        "en": "Full name",
        "fr": "Nom complet",
    },
    "admin.user.title": {
        "en": "Job title",
        "fr": "Fonction",
    },
    "admin.user.group": {
        "en": "Group",
        "fr": "Groupe",
    },
    "admin.user.genre": {
        "en": "Genre",
        "fr": "Genre",
    },
    "admin.user.color": {
        "en": "Color",
        "fr": "Couleur",
    },
    "admin.user.email": {
        "en": "Email",
        "fr": "Email",
    },
    "admin.user.api_url": {
        "en": "API URL",
        "fr": "URL de l'API",
    },
    "admin.user.token": {
        "en": "API Token (plaintext)",
        "fr": "Token API (en clair)",
    },
    "admin.user.add": {
        "en": "Add user",
        "fr": "Ajouter l'utilisateur",
    },
    "admin.user.random": {
        "en": "Random",
        "fr": "Aléatoire",
    },
    "admin.user.lookup": {
        "en": "Fetch user info from API",
        "fr": "Récupérer les infos utilisateur depuis l'API",
    },
    "admin.user.fetched_from_api": {
        "en": "Fetched from API",
        "fr": "Récupéré depuis l'API",
    },
    "admin.user.looking_up": {
        "en": "Fetching user info...",
        "fr": "Récupération des infos...",
    },
    "admin.user.lookup_ok": {
        "en": "User info loaded",
        "fr": "Infos utilisateur chargées",
    },
    "admin.user.lookup_fail": {
        "en": "Could not fetch user info",
        "fr": "Impossible de récupérer les infos utilisateur",
    },
    "admin.user.empty": {
        "en": "No users yet. Add one above.",
        "fr": "Aucun utilisateur. Ajoutez-en un ci-dessus.",
    },

    # Admin — Prompts
    "admin.prompts": {
        "en": "Demo Prompts",
        "fr": "Prompts de démo",
    },
    "admin.prompt.label": {
        "en": "Label",
        "fr": "Libellé",
    },
    "admin.prompt.scope": {
        "en": "Scope",
        "fr": "Portée",
    },
    "admin.prompt.tags": {
        "en": "Tags (comma-separated)",
        "fr": "Tags (séparés par des virgules)",
    },
    "admin.prompt.text": {
        "en": "Prompt text",
        "fr": "Texte du prompt",
    },
    "admin.prompt.add": {
        "en": "Add prompt",
        "fr": "Ajouter le prompt",
    },
    "admin.prompt.empty": {
        "en": "No prompts yet. Add one above.",
        "fr": "Aucun prompt. Ajoutez-en un ci-dessus.",
    },

    # Login
    "login.title": {
        "en": "Welcome",
        "fr": "Bienvenue",
    },
    "login.subtitle": {
        "en": "Select your profile to continue",
        "fr": "Sélectionnez votre profil pour continuer",
    },
    "login.password": {
        "en": "Password",
        "fr": "Mot de passe",
    },
    "login.signin": {
        "en": "Sign in",
        "fr": "Se connecter",
    },
    "login.select_prompt": {
        "en": "Select a profile",
        "fr": "Sélectionnez un profil",
    },
    "login.no_users": {
        "en": "No demo users configured yet.",
        "fr": "Aucun utilisateur de démo configuré.",
    },

    # App
    "app.welcome": {
        "en": "Welcome",
        "fr": "Bienvenue",
    },
    "app.ready": {
        "en": "Chat interface coming next",
        "fr": "Interface de chat à venir",
    },
    "app.switch_user": {
        "en": "Switch user",
        "fr": "Changer d'utilisateur",
    },
    "app.partitions": {
        "en": "Partitions",
        "fr": "Partitions",
    },
    "app.empty_chat": {
        "en": "Start a conversation",
        "fr": "Démarrez une conversation",
    },
    "app.placeholder": {
        "en": "Type a message...",
        "fr": "Écrivez un message...",
    },
    "app.logout": {
        "en": "Log out",
        "fr": "Se déconnecter",
    },
    "app.language": {
        "en": "Language",
        "fr": "Langue",
    },
    "app.theme": {
        "en": "Theme",
        "fr": "Thème",
    },
    "app.theme.dark": {
        "en": "Dark",
        "fr": "Sombre",
    },
    "app.theme.light": {
        "en": "Light",
        "fr": "Clair",
    },
    "app.admin": {
        "en": "Administration",
        "fr": "Administration",
    },
    "app.history": {
        "en": "History",
        "fr": "Historique",
    },
    "app.no_history": {
        "en": "No messages yet",
        "fr": "Aucun message",
    },
    "app.no_files": {
        "en": "No files",
        "fr": "Aucun fichier",
    },
    "app.delete_file": {
        "en": "Delete file",
        "fr": "Supprimer le fichier",
    },
    "app.confirm_delete_file": {
        "en": "Delete {file}?",
        "fr": "Supprimer {file} ?",
    },
    "tooltip.view_file": {
        "en": "View file",
        "fr": "Voir le fichier",
    },
    "tooltip.view_chunk": {
        "en": "View chunk",
        "fr": "Voir le fragment",
    },
    "tooltip.open_new_tab": {
        "en": "Open in new tab",
        "fr": "Ouvrir dans un nouvel onglet",
    },
    "tooltip.manage_access": {
        "en": "Manage access",
        "fr": "Gérer les accès",
    },
    "app.no_access": {
        "en": "No users",
        "fr": "Aucun utilisateur",
    },

    # Chat errors
    "chat.error.unavailable": {
        "en": "The OpenRAG server is currently unavailable. Please try again later or contact your administrator.",
        "fr": "Le serveur OpenRAG est actuellement indisponible. Veuillez réessayer plus tard ou contacter votre administrateur.",
    },
    "chat.error.timeout": {
        "en": "The request took too long. The server may be overloaded — please try again in a moment.",
        "fr": "La requête a pris trop de temps. Le serveur est peut-être surchargé — veuillez réessayer dans un instant.",
    },
    "chat.error.embedding": {
        "en": "The AI embedding service is temporarily down. This is an infrastructure issue on the OpenRAG server — not something you can fix. Please notify your administrator.",
        "fr": "Le service d'embeddings IA est temporairement indisponible. Il s'agit d'un problème d'infrastructure sur le serveur OpenRAG — ce n'est pas de votre ressort. Veuillez prévenir votre administrateur.",
    },
    "chat.error.auth": {
        "en": "Your access token was rejected by the server. It may have expired or been revoked. Please contact your administrator.",
        "fr": "Votre jeton d'accès a été refusé par le serveur. Il a peut-être expiré ou été révoqué. Veuillez contacter votre administrateur.",
    },
    "chat.error.generic": {
        "en": "Something went wrong while contacting the OpenRAG server. Please try again or contact your administrator.",
        "fr": "Une erreur est survenue lors de la communication avec le serveur OpenRAG. Veuillez réessayer ou contacter votre administrateur.",
    },

    # Tooltips
    "tooltip.openrag_playground": {
        "en": "OpenRAG Playground",
        "fr": "OpenRAG Playground",
    },
    "tooltip.active_partition": {
        "en": "Active partition",
        "fr": "Partition active",
    },
    "tooltip.current_partition": {
        "en": "Current partition",
        "fr": "Partition actuelle",
    },
    "tooltip.user_group": {
        "en": "User group",
        "fr": "Groupe utilisateur",
    },
    "tooltip.user_menu": {
        "en": "User menu",
        "fr": "Menu utilisateur",
    },
    "tooltip.sign_out": {
        "en": "Sign out",
        "fr": "Se déconnecter",
    },
    "tooltip.type_message": {
        "en": "Type your message",
        "fr": "Écrivez votre message",
    },
    "tooltip.send_message": {
        "en": "Send message",
        "fr": "Envoyer le message",
    },
    "tooltip.start_conversation": {
        "en": "Start a conversation",
        "fr": "Démarrez une conversation",
    },
    "tooltip.reuse_prompt": {
        "en": "Click to reuse this prompt",
        "fr": "Cliquer pour réutiliser ce prompt",
    },
    "tooltip.partition_used": {
        "en": "Partition used",
        "fr": "Partition utilisée",
    },
    "tooltip.sent_to": {
        "en": "Sent to partition",
        "fr": "Envoyé à la partition",
    },
    "tooltip.sign_in_as": {
        "en": "Sign in as",
        "fr": "Se connecter en tant que",
    },
    "tooltip.group": {
        "en": "Group",
        "fr": "Groupe",
    },
    "tooltip.prefilled_password": {
        "en": "Pre-filled password",
        "fr": "Mot de passe pré-rempli",
    },
    "tooltip.sign_in_start": {
        "en": "Sign in to start chatting",
        "fr": "Connectez-vous pour commencer",
    },
    "tooltip.enter_password": {
        "en": "Enter admin password",
        "fr": "Entrez le mot de passe administrateur",
    },
    "tooltip.unlock": {
        "en": "Unlock the playground",
        "fr": "Déverrouiller le playground",
    },
    "tooltip.visit_openrag": {
        "en": "Visit Open-RAG.ai",
        "fr": "Visiter Open-RAG.ai",
    },
    "tooltip.about": {
        "en": "About OpenRAG Playground",
        "fr": "À propos d'OpenRAG Playground",
    },
    "tooltip.data_protection": {
        "en": "Data protection notice",
        "fr": "Avis de protection des données",
    },
    "tooltip.ai_transparency": {
        "en": "AI transparency notice",
        "fr": "Avis de transparence IA",
    },
    "tooltip.digital_sovereignty": {
        "en": "Digital sovereignty",
        "fr": "Souveraineté numérique",
    },
    "tooltip.legal_notice": {
        "en": "Legal notice",
        "fr": "Mentions légales",
    },
    "tooltip.api_version": {
        "en": "OpenRAG API version",
        "fr": "Version de l'API OpenRAG",
    },
    "tooltip.visit_linagora": {
        "en": "Visit LINAGORA.com",
        "fr": "Visiter LINAGORA.com",
    },
    "tooltip.manage_groups": {
        "en": "Manage groups",
        "fr": "Gérer les groupes",
    },
    "tooltip.manage_users": {
        "en": "Manage demo users",
        "fr": "Gérer les utilisateurs de démo",
    },
    "tooltip.manage_prompts": {
        "en": "Manage demo prompts",
        "fr": "Gérer les prompts de démo",
    },
    "tooltip.back_to_app": {
        "en": "Return to demo login",
        "fr": "Retour à la connexion démo",
    },
    "tooltip.upload_file": {
        "en": "Upload a file",
        "fr": "Envoyer un fichier",
    },
    "tooltip.upload_select_partition": {
        "en": "Select a partition to upload a file",
        "fr": "Sélectionnez une partition pour envoyer un fichier",
    },
    "tooltip.upload_viewer": {
        "en": "You don't have permission to upload to this partition",
        "fr": "Vous n'avez pas la permission d'envoyer des fichiers sur cette partition",
    },
    "app.upload.uploading": {
        "en": "Uploading",
        "fr": "Envoi en cours",
    },
    "app.upload.indexing": {
        "en": "Indexing",
        "fr": "Indexation en cours",
    },
    "app.upload.success": {
        "en": "Uploaded",
        "fr": "Envoyé",
    },
    "app.upload.error": {
        "en": "Upload failed",
        "fr": "Échec de l'envoi",
    },
    "tooltip.save_prompt": {
        "en": "Save as demo prompt",
        "fr": "Enregistrer comme prompt de démo",
    },
    "tooltip.clear_history": {
        "en": "Clear history",
        "fr": "Effacer l'historique",
    },
    "tooltip.stop_streaming": {
        "en": "Stop",
        "fr": "Arrêter",
    },
    "app.save_prompt.global": {
        "en": "For everyone",
        "fr": "Pour tout le monde",
    },
    "app.save_prompt.group": {
        "en": "For my group",
        "fr": "Pour mon groupe",
    },
    "app.save_prompt.partition": {
        "en": "For this partition",
        "fr": "Pour cette partition",
    },
    "app.save_prompt.user": {
        "en": "For me only",
        "fr": "Pour moi uniquement",
    },
    "tooltip.clear_chat": {
        "en": "Clear conversation",
        "fr": "Effacer la conversation",
    },
    "tooltip.select_partition": {
        "en": "Select partition",
        "fr": "Sélectionner la partition",
    },
    "tooltip.toggle_theme": {
        "en": "Toggle theme",
        "fr": "Changer de thème",
    },
    "tooltip.language": {
        "en": "Language",
        "fr": "Langue",
    },

    # Footer modals
    "modal.about.title": {
        "en": "About OpenRAG Playground",
        "fr": "À propos d'OpenRAG Playground",
    },
    "modal.about.body": {
        "en": """
<p><strong>OpenRAG Playground</strong> is a demonstration interface for <a href="https://open-rag.ai" target="_blank" rel="noopener" style="color:var(--accent);">Open-RAG</a>, the sovereign Retrieval-Augmented Generation platform.</p>
<p class="mt-3">Built for live demos and client presentations, it lets operators showcase Open-RAG's capabilities through realistic persona-based scenarios — each backed by real API tokens and access controls.</p>
<p class="mt-3">Developed by <a href="https://linagora.com" target="_blank" rel="noopener" style="color:var(--accent);">LINAGORA</a>, a European open-source software company dedicated to digital sovereignty.</p>
<p class="mt-3" style="color:var(--text-subtle);">Licensed under AGPL-3.0.</p>
""",
        "fr": """
<p><strong>OpenRAG Playground</strong> est une interface de démonstration pour <a href="https://open-rag.ai" target="_blank" rel="noopener" style="color:var(--accent);">Open-RAG</a>, la plateforme souveraine de Génération Augmentée par Recherche.</p>
<p class="mt-3">Conçue pour les démonstrations en direct et les présentations clients, elle permet aux opérateurs de présenter les capacités d'Open-RAG à travers des scénarios réalistes basés sur des personas — chacun adossé à de vrais tokens API et contrôles d'accès.</p>
<p class="mt-3">Développé par <a href="https://linagora.com" target="_blank" rel="noopener" style="color:var(--accent);">LINAGORA</a>, éditeur européen de logiciels libres dédié à la souveraineté numérique.</p>
<p class="mt-3" style="color:var(--text-subtle);">Licence AGPL-3.0.</p>
""",
    },

    "modal.gdpr.title": {
        "en": "Data Protection (GDPR)",
        "fr": "Protection des données (RGPD)",
    },
    "modal.gdpr.body": {
        "en": """
<p><strong>Legal basis.</strong> The processing of personal data is based on the performance of a contract (Article 6(1)(b) GDPR). Your data is processed as necessary to provide you with the service you are using.</p>
<p class="mt-3"><strong>Data processed.</strong> Documents uploaded to the platform, queries submitted to the AI system, and associated metadata (timestamps, partition names). API access tokens are stored encrypted on the server.</p>
<p class="mt-3"><strong>Zero external requests.</strong> This application makes no requests to any third-party service. All assets (fonts, scripts, styles) are self-hosted. Your browser communicates only with the server hosting this application.</p>
<p class="mt-3"><strong>No tracking.</strong> No analytics, no fingerprinting, no advertising. The only cookie used is a signed, httpOnly session cookie for authentication, expiring after 24 hours.</p>
<p class="mt-3"><strong>Data retention.</strong> Data is retained for the duration of the contract. Uploaded documents are stored on the OpenRAG server infrastructure. Configuration data is stored locally on the application server.</p>
<p class="mt-3"><strong>Your rights.</strong> You have the right to access, rectify, erase, restrict, and port your personal data, as well as to object to processing. Contact the DPO to exercise your rights.</p>
<p class="mt-3"><strong>Data controller:</strong> LINAGORA SAS, Villa Good Tech, 37 rue Pierre Poli, 92130 Issy-les-Moulineaux, France.</p>
<p class="mt-3"><strong>DPO:</strong> <span style="color:var(--accent);">dpo@linagora.com</span></p>
""",
        "fr": """
<p><strong>Base légale.</strong> Le traitement des données personnelles repose sur l'exécution d'un contrat (Article 6(1)(b) du RGPD). Vos données sont traitées dans la mesure nécessaire à la fourniture du service que vous utilisez.</p>
<p class="mt-3"><strong>Données traitées.</strong> Documents téléversés sur la plateforme, requêtes soumises au système d'IA, et métadonnées associées (horodatages, noms de partitions). Les tokens d'accès API sont stockés chiffrés sur le serveur.</p>
<p class="mt-3"><strong>Zéro requête externe.</strong> Cette application n'effectue aucune requête vers un service tiers. Toutes les ressources (polices, scripts, styles) sont hébergées localement. Votre navigateur ne communique qu'avec le serveur hébergeant cette application.</p>
<p class="mt-3"><strong>Aucun traçage.</strong> Pas d'analytics, pas de fingerprinting, pas de publicité. Le seul cookie utilisé est un cookie de session signé et httpOnly pour l'authentification, expirant après 24 heures.</p>
<p class="mt-3"><strong>Conservation des données.</strong> Les données sont conservées pendant la durée du contrat. Les documents téléversés sont stockés sur l'infrastructure du serveur OpenRAG. Les données de configuration sont stockées localement sur le serveur applicatif.</p>
<p class="mt-3"><strong>Vos droits.</strong> Vous disposez des droits d'accès, de rectification, d'effacement, de limitation, de portabilité de vos données personnelles, ainsi que du droit d'opposition au traitement. Contactez le DPO pour exercer vos droits.</p>
<p class="mt-3"><strong>Responsable du traitement :</strong> LINAGORA SAS, Villa Good Tech, 37 rue Pierre Poli, 92130 Issy-les-Moulineaux, France.</p>
<p class="mt-3"><strong>DPO :</strong> <span style="color:var(--accent);">dpo@linagora.com</span></p>
""",
    },

    "modal.ai_act.title": {
        "en": "AI Transparency (AI Act)",
        "fr": "Transparence IA (AI Act)",
    },
    "modal.ai_act.body": {
        "en": """
<p>In accordance with the European AI Act (Regulation EU 2024/1689), we provide the following transparency information:</p>
<p class="mt-3"><strong>AI system:</strong> This application is a user interface to <a href="https://open-rag.ai" target="_blank" rel="noopener" style="color:var(--accent);">Open-RAG</a>, a Retrieval-Augmented Generation (RAG) system.</p>
<p class="mt-3"><strong>Purpose:</strong> Answer user questions by retrieving relevant documents from a knowledge base and generating natural language responses.</p>
<p class="mt-3"><strong>How it works:</strong> When you ask a question, the system searches indexed documents for relevant passages, then uses a large language model to generate an answer grounded in those sources. Cited sources are displayed alongside answers.</p>
<p class="mt-3"><strong>Risk classification:</strong> This system is not classified as high-risk under the AI Act. It serves as a productivity and information retrieval tool.</p>
<p class="mt-3"><strong>Human oversight:</strong> All responses should be verified by the user. The system may produce inaccurate or incomplete answers. Sources are provided for verification.</p>
<p class="mt-3"><strong>Provider:</strong> LINAGORA — <a href="https://linagora.com" target="_blank" rel="noopener" style="color:var(--accent);">linagora.com</a></p>
""",
        "fr": """
<p>Conformément au Règlement européen sur l'intelligence artificielle (AI Act, Règlement UE 2024/1689), nous fournissons les informations de transparence suivantes :</p>
<p class="mt-3"><strong>Système d'IA :</strong> Cette application est une interface utilisateur pour <a href="https://open-rag.ai" target="_blank" rel="noopener" style="color:var(--accent);">Open-RAG</a>, un système de Génération Augmentée par Recherche (RAG).</p>
<p class="mt-3"><strong>Finalité :</strong> Répondre aux questions des utilisateurs en recherchant des documents pertinents dans une base de connaissances et en générant des réponses en langage naturel.</p>
<p class="mt-3"><strong>Fonctionnement :</strong> Lorsque vous posez une question, le système recherche des passages pertinents dans les documents indexés, puis utilise un grand modèle de langage pour générer une réponse fondée sur ces sources. Les sources citées sont affichées avec les réponses.</p>
<p class="mt-3"><strong>Classification de risque :</strong> Ce système n'est pas classé comme à haut risque au sens de l'AI Act. Il sert d'outil de productivité et de recherche d'information.</p>
<p class="mt-3"><strong>Supervision humaine :</strong> Toutes les réponses doivent être vérifiées par l'utilisateur. Le système peut produire des réponses inexactes ou incomplètes. Les sources sont fournies pour vérification.</p>
<p class="mt-3"><strong>Fournisseur :</strong> LINAGORA — <a href="https://linagora.com" target="_blank" rel="noopener" style="color:var(--accent);">linagora.com</a></p>
""",
    },

    "modal.sovereignty.title": {
        "en": "Data Sovereignty",
        "fr": "Souveraineté des données",
    },
    "modal.sovereignty.body": {
        "en": """
<p><strong>OpenRAG Playground</strong> is designed with European digital sovereignty at its core.</p>
<p class="mt-3"><strong>Self-hosted.</strong> The entire application runs on your infrastructure. No cloud dependency, no SaaS lock-in.</p>
<p class="mt-3"><strong>Zero external requests.</strong> The application makes no calls to any external service. All assets are vendored locally. Your browser communicates only with your server.</p>
<p class="mt-3"><strong>Open source.</strong> The full source code is available under AGPL-3.0, ensuring transparency, auditability, and freedom from vendor lock-in.</p>
<p class="mt-3"><strong>European provider.</strong> Built by <a href="https://linagora.com" target="_blank" rel="noopener" style="color:var(--accent);">LINAGORA</a>, headquartered in Toulouse, France. Subject to European law and GDPR.</p>
<p class="mt-3"><strong>Your data stays yours.</strong> Documents, tokens, and configuration never leave your infrastructure. No telemetry, no data sharing, no third-party processing.</p>
""",
        "fr": """
<p><strong>OpenRAG Playground</strong> est conçu avec la souveraineté numérique européenne au cœur de son architecture.</p>
<p class="mt-3"><strong>Auto-hébergé.</strong> L'application complète fonctionne sur votre infrastructure. Aucune dépendance cloud, aucun enfermement SaaS.</p>
<p class="mt-3"><strong>Zéro requête externe.</strong> L'application n'effectue aucun appel vers un service externe. Toutes les ressources sont hébergées localement. Votre navigateur ne communique qu'avec votre serveur.</p>
<p class="mt-3"><strong>Open source.</strong> Le code source complet est disponible sous licence AGPL-3.0, garantissant transparence, auditabilité et indépendance technologique.</p>
<p class="mt-3"><strong>Fournisseur européen.</strong> Développé par <a href="https://linagora.com" target="_blank" rel="noopener" style="color:var(--accent);">LINAGORA</a>, basé à Toulouse, France. Soumis au droit européen et au RGPD.</p>
<p class="mt-3"><strong>Vos données restent les vôtres.</strong> Documents, tokens et configuration ne quittent jamais votre infrastructure. Pas de télémétrie, pas de partage de données, pas de traitement par des tiers.</p>
""",
    },

    "modal.legal.title": {
        "en": "Legal Notice",
        "fr": "Mentions légales",
    },
    "modal.legal.body": {
        "en": """
<p><strong>Publisher</strong></p>
<p>LINAGORA SAS<br>
Villa Good Tech, 37 rue Pierre Poli<br>
92130 Issy-les-Moulineaux, France<br>
RCS Nanterre — SIREN 431 473 669<br>
<a href="https://linagora.com" target="_blank" rel="noopener" style="color:var(--accent);">linagora.com</a></p>
<p class="mt-3"><strong>Director of publication:</strong> Michel-Marie Maudet</p>
<p class="mt-3"><strong>Hosting</strong></p>
<p>Hosted in France by OVHcloud — <a href="https://www.ovhcloud.com/fr/terms-and-conditions/" target="_blank" rel="noopener" style="color:var(--accent);">Terms and conditions</a></p>
<p class="mt-3"><strong>Intellectual property</strong></p>
<p>OpenRAG Playground is free software licensed under AGPL-3.0. Open-RAG is a trademark of LINAGORA. LINAGORA and the LINAGORA logo are trademarks of LINAGORA SAS.</p>
<p class="mt-3"><strong>Contact:</strong> <span style="color:var(--accent);">contact@linagora.com</span></p>
""",
        "fr": """
<p><strong>Éditeur</strong></p>
<p>LINAGORA SAS<br>
Villa Good Tech, 37 rue Pierre Poli<br>
92130 Issy-les-Moulineaux, France<br>
RCS Nanterre — SIREN 431 473 669<br>
<a href="https://linagora.com" target="_blank" rel="noopener" style="color:var(--accent);">linagora.com</a></p>
<p class="mt-3"><strong>Directeur de la publication :</strong> Michel-Marie Maudet</p>
<p class="mt-3"><strong>Hébergement</strong></p>
<p>Hébergé en France par OVHcloud — <a href="https://www.ovhcloud.com/fr/terms-and-conditions/" target="_blank" rel="noopener" style="color:var(--accent);">Conditions générales</a></p>
<p class="mt-3"><strong>Propriété intellectuelle</strong></p>
<p>OpenRAG Playground est un logiciel libre sous licence AGPL-3.0. Open-RAG est une marque de LINAGORA. LINAGORA et le logo LINAGORA sont des marques de LINAGORA SAS.</p>
<p class="mt-3"><strong>Contact :</strong> <span style="color:var(--accent);">contact@linagora.com</span></p>
""",
    },

    # Partition stats
    "stats.file": {
        "en": "doc",
        "fr": "doc",
    },
    "stats.files": {
        "en": "docs",
        "fr": "docs",
    },
    "stats.chunk": {
        "en": "chunk",
        "fr": "fragment",
    },
    "stats.chunks": {
        "en": "chunks",
        "fr": "fragments",
    },

    # Documents panel
    "docs.quota": {
        "en": "Quota",
        "fr": "Quota",
    },
    "docs.files_used": {
        "en": "files used",
        "fr": "fichiers utilisés",
    },
    "docs.by_type": {
        "en": "By type",
        "fr": "Par type",
    },
    "docs.growth": {
        "en": "Growth",
        "fr": "Croissance",
    },
    "docs.last_10_days": {
        "en": "last 10 days",
        "fr": "10 derniers jours",
    },
    "docs.indexed": {
        "en": "Indexed",
        "fr": "Indexés",
    },
    "docs.pending": {
        "en": "Pending",
        "fr": "En attente",
    },
    "docs.total": {
        "en": "Total",
        "fr": "Total",
    },
    "docs.title": {
        "en": "Documents",
        "fr": "Documents",
    },

    # Roles
    "role.none": {
        "en": "No access",
        "fr": "Aucun accès",
    },
    "role.viewer": {
        "en": "Viewer",
        "fr": "Lecteur",
    },
    "role.editor": {
        "en": "Editor",
        "fr": "Éditeur",
    },
    "role.owner": {
        "en": "Owner",
        "fr": "Propriétaire",
    },
}


def get_locale() -> str:
    """Get current locale: session override > Accept-Language > 'en'."""
    if "lang" in session:
        return session["lang"]
    best = request.accept_languages.best_match(["en", "fr"], default="en")
    return best


def t(key: str) -> str:
    """Translate a key to the current locale."""
    lang = get_locale()
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get("en", key))


def init_i18n(app: Flask):
    """Register t() and lang as Jinja2 globals, plus /set-language route."""

    @app.context_processor
    def inject_i18n():
        return {"t": t, "lang": get_locale}

    @app.route("/set-language", methods=["POST"])
    def set_language():
        lang = request.form.get("lang", "en")
        if lang in ("en", "fr"):
            session["lang"] = lang
        # Return empty response for HTMX to trigger page refresh
        from flask import make_response
        resp = make_response("")
        resp.headers["HX-Refresh"] = "true"
        return resp
