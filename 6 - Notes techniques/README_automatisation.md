# Automatisation de la Synchronisation Git Horodatée

Ce document résume les étapes pour configurer une synchronisation automatique (commit et push) du dépôt Git local (`00_Vault_SAVOIR`) vers un dépôt distant toutes les heures, en prenant en compte une clé SSH protégée par une passphrase.

## 1. Prérequis : Gestion de la clé SSH avec Passphrase

Pour que le script puisse s'exécuter sans intervention manuelle (saisie de la passphrase), il est nécessaire d'ajouter la clé à l'agent SSH et d'enregistrer la passphrase dans le Trousseau d'accès (Keychain) de macOS.

Cette commande doit être exécutée une seule fois dans le terminal :
```bash
ssh-add -K ~/.ssh/id_rsa
```
*(Remplacez `~/.ssh/id_rsa` si votre clé privée porte un autre nom.)*

## 2. Création du Script d'Automatisation

Un script shell a été créé pour gérer la logique de commit et de push.

-   **Emplacement du script** : `/Users/walidnamane/git_push_script.sh`
-   **Contenu du script** :
    ```shell
    #!/bin/zsh
    cd /Users/walidnamane/Documents/SAVOIR/00_Vault_SAVOIR

    # Vérifie s'il y a des changements à commiter
    if [[ -n $(git status --porcelain) ]]; then
      git add .
      git commit -m "Commit automatisé du $(date)"
      git push
    fi
    ```

-   **Rendre le script exécutable** :
    Pour que `cron` puisse exécuter le script, celui-ci doit avoir les permissions d'exécution.
    ```bash
    chmod +x /Users/walidnamane/git_push_script.sh
    ```

## 3. Configuration de la Tâche Cron

Une tâche `cron` a été configurée pour lancer le script automatiquement toutes les heures.

-   **Commande d'ajout** :
    ```bash
    (crontab -l 2>/dev/null; echo "0 * * * * /Users/walidnamane/git_push_script.sh") | crontab -
    ```
-   **Signification** : L'entrée `0 * * * *` signifie "à la minute 0, de chaque heure, de chaque jour".

## 4. Tester le Processus

Pour vérifier que tout fonctionne sans attendre la prochaine heure :
1.  Modifiez un fichier dans le répertoire `/Users/walidnamane/Documents/SAVOIR/00_Vault_SAVOIR`.
2.  Exécutez le script manuellement avec la commande :
    ```bash
    /Users/walidnamane/git_push_script.sh
    ```
3.  Vérifiez sur votre dépôt distant (par exemple, sur GitHub) que le nouveau commit est bien apparu.
