# Conception de la base de données

La première version utilise SQLite pour le prototype.

## Tables
- members : identité interne des membres.
- roles : catalogue des rôles.
- member_roles : associations entre membres et rôles.
- consent_records : historique des consentements.
- audit_logs : journal des événements techniques et de sécurité.

## Sécurité et confidentialité
- Clés étrangères activées.
- Identifiants internes aléatoires.
- Collecte minimale.
- Aucun secret d'authentification dans les profils.
- Les journaux ne doivent pas contenir de mots de passe,
  jetons ou données personnelles sensibles.

## Évolution
Une migration vers PostgreSQL pourra être réalisée lorsque
l'hébergement et les besoins de charge le justifieront.
