# Projet Therion - Topographie Spéléologique

Ce projet fournit un ensemble d'outils Python pour faciliter la création et la gestion de topographies de cavités avec [Therion](https://therion.speleo.sk/), le logiciel de topographie spéléologique.

## 📋 Table des matières

- [Description](#description)
- [Prérequis](#prérequis)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [1. Créer un nouveau projet](#1-créer-un-nouveau-projet)
  - [2. Générer les scraps depuis un XVI](#2-générer-les-scraps-depuis-un-xvi)
  - [3. Nettoyer les fichiers .th2](#3-nettoyer-les-fichiers-th2)
  - [4. Compiler les projets Therion](#4-compiler-les-projets-therion)
- [Scripts disponibles](#scripts-disponibles)
- [Format des fichiers](#format-des-fichiers)
- [Workflow recommandé](#workflow-recommandé)
- [Dépannage](#dépannage)
- [Conseils et bonnes pratiques](#conseils-et-bonnes-pratiques)
- [Ressources](#ressources)
- [Auteur](#auteur)
- [Licence](#licence)
- [Contributions](#contributions)
- [Changelog](#changelog)

## Description

Ce projet automatise plusieurs tâches répétitives dans le workflow de topographie spéléologique :

- **Création de structure de projet** : génère automatiquement l'arborescence complète d'un nouveau projet Therion
- **Génération de scraps** : crée automatiquement les scraps plan et coupe depuis les export (.xvi)
- **Nettoyage des fichiers** : supprime les objets vides (lines/areas) dans les fichiers .th2
- **Compilation en masse** : compile tous les projets Therion d'un répertoire en une seule commande

## Prérequis

### Logiciels requis

- **Python 3.7+** ([télécharger](https://www.python.org/downloads/))
- **Therion 6.x** ([télécharger](https://therion.speleo.sk/downloads.html))

### Bibliothèques Python

Aucune bibliothèque externe n'est requise. Les scripts utilisent uniquement la bibliothèque standard Python.

## Structure du projet

```
projet-therion/
│
├── Templates/                      # Templates pour nouveaux projets
│   ├── CAVENAME.thconfig          # Configuration principale
│   ├── CAVENAME-tot.th            # Fichier principal de survey
│   ├── CAVENAME-maps.th           # Définition des maps
│   ├── CAVENAME-plan.th2          # Template plan
│   ├── CAVENAME-coupe.th2         # Template coupe
│   └── config.thc                 # Configuration globale
│
├── Create_survey_structure.py     # Création nouveau projet
├── Create_scrap.py                # Génération scraps depuis .xvi
├── Clean_th2.py                   # Nettoyage fichiers .th2
├── run_all.py                     # Compilation en masse
│
└── nom_de_votre_cavite/           # Projet généré
    ├── Data/                      # Données sources
    │   ├── cavite.th              # Mesures TopoDroid
    │   ├── cavite.th2             # Dessin TopoDroid
    │   ├── cavite-plan.th2        # Scraps plan
    │   ├── cavite-coupe.th2       # Scraps coupe
    │   ├── cavite-map.xvi         # Export XVI plan
    │   └── cavite-coupe.xvi       # Export XVI coupe
    │
    ├── Outputs/                   # Fichiers générés
    │   ├── cavite-plan.pdf        # Plan final
    │   ├── cavite-coupe.pdf       # Coupe finale
    │   ├── cavite.lox             # Modèle 3D
    │   ├── cavite.kml             # Export KML
    │   └── questions.html         # Liste continuations
    │
    ├── cavite.thconfig            # Config principale
    ├── cavite-tot.th              # Survey principal
    ├── cavite-maps.th             # Maps du projet
    └── config.thc                 # Config partagée
```

## Installation

### 1. Cloner ou télécharger le projet

```bash
git clone https://github.com/votre-repo/projet-therion.git
cd projet-therion
```

### 2. Configurer le dossier Templates

Assurez-vous que le dossier `Templates/` contient tous les fichiers templates nécessaires :

- `CAVENAME.thconfig`
- `CAVENAME-tot.th`
- `CAVENAME-maps.th`
- `CAVENAME-plan.th2`
- `CAVENAME-coupe.th2`
- `config.thc`

### 3. Vérifier l'installation de Therion

```bash
therion --version
```

Devrait afficher : `therion 6.x.x`

## Utilisation

### 1. Créer un nouveau projet

#### Option A : Projet vide (sans données TopoDroid)

```bash
python Create_survey_structure.py gouffre_berger --empty-th2
```

Cela crée :
- L'arborescence complète du projet
- Les fichiers .th2 vides prêts à être dessinés

#### Option B : Import depuis TopoDroid

```bash
python Create_survey_structure.py gouffre_berger --th export.th --th2 export.th2
```

Cela crée :
- L'arborescence complète
- Importe vos données TopoDroid dans `Data/`

**Paramètres :**
- `gouffre_berger` : nom du projet (A-Z, a-z, 0-9, _, -)
- `--th` : chemin vers le fichier `.th` de TopoDroid
- `--th2` : chemin vers le fichier `.th2` de TopoDroid
- `--empty-th2` : crée des fichiers .th2 vides

### 2. Générer les scraps depuis un XVI

Après avoir exporté vos fichiers `.xvi` en faisant tourner une première fois Therion :

```bash
python Create_scrap.py chemin/vers/gouffre_berger/gouffre_berger.th
```

**Ce script fait quoi ?**

1. ✅ Lit les fichiers `.xvi` (plan et coupe)
2. ✅ Extrait toutes les stations topographiques
3. ✅ Génère automatiquement des scraps par groupe de 10 stations
4. ✅ Ajoute les scraps aux fichiers `.th2` correspondants
5. ✅ Met à jour le fichier `-maps.th` avec les références

**Fichiers générés :**

```
Data/gouffre_berger-plan.th2   → Contient SP-gouffre_berger-1, SP-gouffre_berger-2...
Data/gouffre_berger-coupe.th2  → Contient SC-gouffre_berger-1, SC-gouffre_berger-2...
gouffre_berger-maps.th         → Référence tous les scraps
```

**Note :** Les scraps sont générés avec la projection correcte :
- Plan : `-projection plan`
- Coupe : `-projection extended`

### 3. Nettoyer les fichiers .th2

Pour supprimer les objets vides (lines/areas vides) de vos fichiers `.th2` :

```bash
python Clean_th2.py
```

**⚠️ Modifier le chemin dans le script avant exécution !**

Éditez `Clean_th2.py` ligne 56 :
```python
dossier = r"C:\Users\votre_nom\Documents\Spéléo\Topographie"
```

Le script parcourt récursivement tous les `.th2` et supprime :
- `line ... endline` vides
- `area ... endarea` vides

**Résultat :**
```
fichier1.th2 -> 3 line(s) supprimée(s), 1 area(s) supprimée(s)
fichier2.th2 -> 0 line(s) supprimée(s), 5 area(s) supprimée(s)

===== RÉSUMÉ =====
Fichiers traités : 12
Lines supprimées : 45
Areas supprimées : 23
```

### 4. Compiler les projets Therion

#### Compiler un seul projet

```bash
cd gouffre_berger
therion gouffre_berger.thconfig
```

#### Compiler tous les projets d'un dossier

```bash
python run_all.py /chemin/vers/projets/
```

**Options disponibles :**

```bash
# Mode verbeux (affiche les commandes)
python run_all.py /chemin/vers/projets/ -v

# Test sans exécution (dry-run)
python run_all.py /chemin/vers/projets/ -n

# Arrêter à la première erreur
python run_all.py /chemin/vers/projets/ --stop-on-error
```

**Résultat :**
```
[INFO] 5 fichiers

[DIR] /home/user/projets/grotte1
[CMD] cd "/home/user/projets/grotte1" && therion "grotte1.thconfig"

[DIR] /home/user/projets/grotte2
[CMD] cd "/home/user/projets/grotte2" && therion "grotte2.thconfig"

OK=4 FAIL=1
```

## Scripts disponibles

### Create_survey_structure.py

Crée un nouveau projet Therion complet depuis les templates.

**Usage :**
```bash
python Create_survey_structure.py <nom_projet> [options]
```

**Options :**
- `--th <fichier>` : Import fichier .th TopoDroid
- `--th2 <fichier>` : Import fichier .th2 TopoDroid
- `--empty-th2` : Crée fichiers .th2 vides

**Exemple :**
```bash
python Create_survey_structure.py reseau_toto --th export_td.th --th2 export_td.th2
```

### Create_scrap.py

Génère automatiquement les scraps depuis les exports XVI.

**Usage :**
```bash
python Create_scrap.py chemin/vers/CAVENAME.th
```

**Détails techniques :**
- Groupe les stations par 10 (modifiable avec `CHUNK_SIZE`)
- Évite les doublons de stations dans un même scrap
- Nomme les scraps : `SP-<cavité>-<n>` (plan) et `SC-<cavité>-<n>` (coupe)
- Associe automatiquement le nom du survey

**Fichiers requis :**
- `CAVENAME.th` : contient le nom du survey
- `CAVENAME-map.xvi` : export XVI plan
- `CAVENAME-coupe.xvi` : export XVI coupe

### Clean_th2.py

Nettoie les fichiers .th2 en supprimant les objets vides.

**Usage :**
```bash
python Clean_th2.py
```

**⚠️ Configuration :** Modifier la variable `dossier` dans le script.

**Objets supprimés :**
```therion
line wall
endline
# ← Supprimé car vide

area sand
endarea
# ← Supprimé car vide
```

### run_all.py

Compile tous les projets Therion d'un répertoire.

**Usage :**
```bash
python run_all.py [chemin] [options]
```

**Options :**
- `-v, --verbose` : Affiche les commandes exécutées
- `-n, --dry-run` : Simule sans exécuter
- `--stop-on-error` : Arrête à la première erreur

**Exemple :**
```bash
python run_all.py ~/Documents/Spéléo/ -v --stop-on-error
```

## Format des fichiers

### Structure d'un projet Therion

```
cavite/
├── cavite.thconfig          # Point d'entrée Therion
├── cavite-tot.th            # Survey principal
├── cavite-maps.th           # Définition des maps
├── config.thc               # Config partagée (layouts, symboles)
│
├── Data/
│   ├── cavite.th            # Données topo (centerline)
│   ├── cavite.th2           # Dessin brut TopoDroid (optionnel)
│   ├── cavite-plan.th2      # Scraps plan + dessins
│   ├── cavite-coupe.th2     # Scraps coupe + dessins
│   ├── cavite-map.xvi       # Export XVI plan
│   └── cavite-coupe.xvi     # Export XVI coupe
│
└── Outputs/
    ├── cavite-plan.pdf
    ├── cavite-coupe.pdf
    ├── cavite-coupe_elevation.pdf
    ├── cavite.lox
    ├── cavite.kml
    ├── cavite.html
    └── questions.html
```

### Fichier .thconfig

Configuration principale du projet. Contient :
- Source des données (`source cavite-tot.th`)
- Layouts d'export (échelles, grilles, légendes)
- Exports multiples (PDF, XVI, KML, LOX, ESRI)

### Fichier .th

Données de mesures topographiques (centerline) :
```therion
survey cavite -title "Grotte de..."
  centerline
    date 2024-01-15
    units length meters
    units compass degrees
    data normal from to length compass clino
    0 1 10.5 45 -5
    1 2 8.3 90 10
  endcenterline
endsurvey
```

### Fichier .th2

Dessins vectoriels (scraps, lignes, zones) :
```therion
scrap SP-cavite-1 -projection plan
  point 100 200 station -name 0
  point 150 250 station -name 1
  
  line wall
    300 100
    350 150
  endline
  
  area water
    400 100
    450 150
  endarea
endscrap
```

### Fichier -maps.th

Définition des maps finales :
```therion
map MP-cavite-plan-tot -title "Plan général"
  SP-cavite-1
  SP-cavite-2
endmap

map MC-cavite-coupe-tot -title "Coupe développée"
  SC-cavite-1
  SC-cavite-2
endmap
```

## Workflow recommandé

### 1. Topographie terrain
- Utilisez TopoDroid pour les mesures
- Exportez régulièrement vos données

### 2. Création du projet
```bash
python Create_survey_structure.py ma_grotte --th export.th
```

### 3. Export XVI 
- Compiler le projet Therion

### 4. Génération des scraps
```bash
python Create_scrap.py ma_grotte/ma_grotte.th
```

### 5. Dessin dans Therion
1. Ouvrez Therion
2. Chargez `ma_grotte.thconfig`
3. Dessinez vos parois, détails, etc. dans les scraps

### 6. Compilation
```bash
cd ma_grotte
therion ma_grotte.thconfig
```

### 7. Vérification
- Consultez `Outputs/ma_grotte-plan.pdf`
- Vérifiez `therion.log` pour les erreurs

### 8. Nettoyage (optionnel)
```bash
python Clean_th2.py
```

### 9. Compilation finale
```bash
python run_all.py ~/Documents/Spéléo/ -v
```

## Dépannage

### Erreur : "can't open file for input"

**Problème :** Le fichier référencé n'existe pas.

**Solution :**
- Vérifiez que tous les fichiers existent dans `Data/`
- Vérifiez les chemins dans `.thconfig` et `-tot.th`
- Les chemins sont relatifs au fichier qui les référence

### Erreur : "No survey found in .th"

**Problème :** Le fichier `.th` ne contient pas de bloc `survey`.

**Solution :**
Assurez-vous que votre fichier `.th` contient :
```therion
survey nom_cavite -title "Titre"
  # contenu
endsurvey
```

### Scraps non visibles sur la carte

**Problème :** Les scraps sont générés mais n'apparaissent pas.

**Solution :**
1. Vérifiez que les scraps sont référencés dans `-maps.th`
2. Décommentez les lignes `select` dans `.thconfig` :
```therion
select MP-cavite-plan-tot@cavite
select MC-cavite-coupe-tot@cavite
```

### Stations en double

**Problème :** Les stations apparaissent plusieurs fois.

**Solution :**
Le script `Create_scrap.py` évite les doublons dans un même scrap. Si le problème persiste :
- Vérifiez vos fichiers `.xvi` source
- Nettoyez manuellement les doublons dans les `.th2`

### Therion non trouvé (Windows)

**Problème :** `[FATAL] therion introuvable`

**Solution :**
Ajoutez Therion au PATH :
1. Panneau de configuration → Système → Paramètres système avancés
2. Variables d'environnement
3. Ajoutez `C:\Program Files\Therion` au PATH

### Encodage des caractères

**Problème :** Caractères accentués mal affichés.

**Solution :**
- Tous les fichiers doivent être en **UTF-8**
- Première ligne de chaque fichier : `encoding utf-8`

### Grille UTM incorrecte

**Problème :** Les coordonnées sont décalées.

**Solution :**
Dans `.thconfig`, ajustez la zone UTM :
```therion
cs UTM32  # Remplacez 32 par votre zone
```

## Conseils et bonnes pratiques

### Nommage des projets
- Utilisez des noms courts et explicites
- Évitez les espaces (utilisez `_` ou `-`)
- Exemples : `grotte_glacee`, `reseau-sud`, `puits23`

### Organisation des données
- Une cavité = un projet
- Utilisez des sous-surveys pour les réseaux complexes
- Gardez `Data/` pour les sources, `Outputs/` pour les exports

### Sauvegarde
- Versionnez avec Git
- Sauvegardez régulièrement `Data/`
- Les fichiers `Outputs/` sont régénérables

### Performance
- Pour de gros projets, utilisez plusieurs maps
- Divisez les scraps complexes
- Commentez les exports inutiles dans `.thconfig`

### Collaboration
- Partagez le dossier `Templates/` dans l'équipe
- Utilisez les mêmes conventions de nommage
- Documentez vos modifications dans les commentaires

## Ressources

### Documentation Therion
- [Site officiel](https://therion.speleo.sk/)
- [Therion Book (manuel)](https://therion.speleo.sk/downloads/thbook.pdf)
- [Wiki Therion](https://therion.speleo.sk/wiki/)

### Logiciels complémentaires
- [TopoDroid](https://sites.google.com/site/speleoapps/) - Saisie terrain Android
- [Survex](https://survex.com/) - Alternative à Therion
- [Loch](https://therion.speleo.sk/) - Visualiseur 3D Therion

## Auteur

**Benoît Urruty**
- Scripts Python pour automatisation Therion
- Templates et workflow optimisés

## Licence

### Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

Ce projet est sous licence **CC BY-NC-SA 4.0**.

![CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)

#### Vous êtes autorisé à :

- **Partager** — copier, distribuer et communiquer le matériel par tous moyens et sous tous formats
- **Adapter** — remixer, transformer et créer à partir du matériel

#### Selon les conditions suivantes :

- **Attribution** — Vous devez créditer l'œuvre, intégrer un lien vers la licence et indiquer si des modifications ont été effectuées. Vous devez indiquer ces informations par tous les moyens raisonnables, sans toutefois suggérer que l'Offrant vous soutient ou soutient la façon dont vous avez utilisé son œuvre.

- **Pas d'Utilisation Commerciale** — Vous n'êtes pas autorisé à faire un usage commercial de cette œuvre, tout ou partie du matériel la composant.

- **Partage dans les Mêmes Conditions** — Dans le cas où vous effectuez un remix, que vous transformez, ou créez à partir du matériel composant l'œuvre originale, vous devez diffuser l'œuvre modifiée dans les mêmes conditions, c'est-à-dire avec la même licence avec laquelle l'œuvre originale a été diffusée.

#### Texte complet de la licence :
[https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.fr](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.fr)

#### Résumé de la licence :
[https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.fr)

## Contributions

Les contributions sont les bienvenues !

Pour contribuer :
1. Forkez le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. Pushez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

**Note :** En contribuant à ce projet, vous acceptez que vos contributions soient distribuées sous la même licence CC BY-NC-SA 4.0.

## Changelog

### Version actuelle
- ✅ Création automatique de projets
- ✅ Génération de scraps depuis XVI
- ✅ Nettoyage des fichiers .th2
- ✅ Compilation en masse
- ✅ Templates configurables

### Améliorations futures
- [ ] Interface graphique (GUI)
- [ ] Gestion des versions de fichiers
- [ ] Validation automatique des fichiers
- [ ] Export automatisé vers cloud
- [ ] Intégration Git automatique
- [ ] Détection automatique de la zone UTM

---

**Bon levé topographique ! 🗻🔦**


# script en cours de création

*create_cave_structure.py* permet de créer les dossiers pour démarrer une topographie de cavité contenant plusieurs survey

*create_scrap.py* script automatique de creation de scrap