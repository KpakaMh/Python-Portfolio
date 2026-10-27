# 🧬 Omics Analytics Dashboard

> Plateforme web interactive et modulaire pour l'exploration, la normalisation et la visualisation de données d'expression génique et biostatistiques omiques.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Dash](https://img.shields.io/badge/Framework-Dash%20%2F%20Plotly-0081CB?logo=plotly)
![Architecture](https://img.shields.io/badge/Architecture-POO%205%20couches-green)
![Tests](https://img.shields.io/badge/Tests-Pytest-yellow?logo=pytest)

---

## 🎯 Aperçu du projet

**Omics Analytics Dashboard** est un outil conçu pour les chercheurs et bioinformaticiens souhaitant analyser rapidement des profils d'expression génique à partir de fichiers CSV hétérogènes. 

L'application intègre un moteur d'ingestion intelligent basé sur des alias de colonnes pour supporter automatiquement divers formats de données (RNA-seq, qPCR, puces à ADN) sans reformatage manuel préalable.

---

## ✨ Fonctionnalités clés

* **Ingestion universelle & nettoyage automatique :**
  * Cartographie dynamique des en-têtes (`gene_symbol`, `sample`, `cpm`, `log2fc`, `pvalue`, etc.).
  * Normalisation automatique des types, suppression des espaces parasites et conversion des décimales.
  * Validation stricte des données de structure.
* **Interface Bioinformatique dédiée :**
  * Thème sombre inspiré des outils d'analyse omique avec filigrane d'ADN et icônes scientifiques FontAwesome.
  * Réactivité complète et cartes de contrôles intégrées.
* **Visualisations interactives (Plotly) :**
  * **Barplot (Expression) :** Comparaison groupée par condition avec affichage exhaustif des gènes sur l'axe X.
  * **Heatmap :** Matrice d'expression (Gènes $\times$ Conditions) pour détecter les profils globaux.
  * **Volcano Plot :** Cartographie de la significativité statistique ($\log_2\text{FC}$ vs $-\log_{10}(P\text{-value})$).
* **Architecture orientée objet (POO) :**
  * Respect du principe *Open/Closed* permettant d'étendre la détection de variables sans modifier les loaders existants.

---

## 🏗️ Architecture du projet

```text
Dashboard/
├── assets/
│   └── style.css              # Style CSS personnalisés (thème sombre, fond ADN)
├── data/
│   └── loaders.py             # Logique d'ingestion POO (DataLoader, CSVLoader, OmicsLoader)
├── tests/
│   └── test_loaders.py        # Suite de tests unitaires (pytest)
├── app.py                     # Application Dash, layouts et callbacks
├── test_omics_10features.csv  # Fichier CSV de démonstration
├── requirements.txt           # Dépendances du projet
└── README.md                  # Documentation
