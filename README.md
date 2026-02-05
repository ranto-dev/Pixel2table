# 💡 Pixel2Table
**Capture d’images via webcam, extraction de caractéristiques visuelles et stockage dans PostgreSQL (Docker)**


## 📌 Description

**Pixel2Table** est une application Python basée sur **OpenCV** permettant de :

* Capturer des images en temps réel via une **webcam**
* Déclencher la capture à l’aide du **clavier (touche ESPACE)**
* Extraire automatiquement des **caractéristiques visuelles** (formes, moments, métriques géométriques)
* Stocker les informations extraites dans une base **PostgreSQL conteneurisée avec Docker**
* Organiser les données dans **trois tables distinctes**, une par image capturée

Ce projet a été réalisé dans un **cadre académique** afin de démontrer l’intégration entre la vision par ordinateur et les bases de données relationnelles.

## 🎯 Objectifs du projet

* Apprendre à utiliser **OpenCV** pour la capture et l’analyse d’images
* Mettre en place une **architecture modulaire Python**
* Utiliser **Docker** pour le déploiement de PostgreSQL
* Structurer et stocker des données complexes dans une base relationnelle
* Gérer une interaction utilisateur simple via le clavier


## 🐳 Base de données (PostgreSQL + Docker)

* PostgreSQL est exécuté dans un **conteneur Docker**
* La base de données s’appelle : `shapes_db`
* Trois tables sont utilisées :

  * `image1_features`
  * `image2_features`
  * `image3_features`

Chaque table stocke :

* Aire
* Périmètre
* Ratio largeur/hauteur
* Circularité
* Solidité
* Moments de Hu
* Histogramme de forme
* Date de création

## 📷 Fonctionnement de l’application

1. L’application démarre et ouvre la **webcam**
2. L’utilisateur appuie sur **ESPACE** pour capturer une image
3. L’opération est répétée **trois fois**
4. Chaque image est :

   * analysée avec OpenCV
   * transformée en caractéristiques numériques
   * insérée dans une table PostgreSQL dédiée
5. Après la troisième capture, le programme affiche :

```
✅ Programme terminé avec succès.
```

---

## ▶️ Lancement de l’application

### 1️⃣ Lancer PostgreSQL avec Docker

```bash
docker compose -f docker/docker-compose.yml up -d
```

---

### 2️⃣ Créer et activer l’environnement virtuel Python

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate    # Windows
```

---

### 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Lancer l’application

```bash
cd src
python main.py
```


## ⌨️ Commandes clavier

| Touche | Action                |
| ------ | --------------------- |
| ESPACE | Capturer une image    |
| Q      | Quitter l’application |


## 📦 Dépendances

* Python 3.9+
* OpenCV
* NumPy
* psycopg2
* Docker & Docker Compose

## 🧪 Vérification des données

```bash
# executer le container docker
sudo docker exec -it pixel2table_db bash

# connexion vers posgrsa
psql -h localhost -U postgres -d shapes_db
```

```sql
SELECT * FROM image1_features;
SELECT * FROM image2_features;
SELECT * FROM image3_features;
```

## 🎓 Contexte académique

Ce projet a été développé dans le cadre d’un **examen**, visant à évaluer :

* la maîtrise de Python
* l’utilisation d’OpenCV
* la conception d’une base de données relationnelle
* l’usage de Docker
* la structuration et la clarté de l’architecture logicielle


## ✨ Améliorations possibles

* Ajout d’une interface graphique
* Normalisation de la base (table unique + clé étrangère)
* Support de plusieurs couleurs / formes
* Sauvegarde locale des images
* Ajout de métriques de confiance

## 👨‍💻 Auteurs

Projet réalisé par :
[**ranto-dev**](https://ranto-dev.vercel.app)
