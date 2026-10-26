### 🧬 Dashboard Omique Interactif — Architecture POO & Dash
**Stack :** Python 3, Dash, Plotly, Pandas, NumPy  
**Auteur :** Kpaka Mouhamadou Adesanya  

Application web interactive dédiée à la visualisation et au contrôle qualité de données d'expression génique, conçue selon les principes d'ingénierie logicielle pour la R&D bioinformatique.

* **Architecture POO découplée (5 couches) :** Séparation stricte de la donnée (`loaders`), de la logique (`filters`), de la vue (`plots`), des retours UI (`notifications`) et de l'orchestration (`app`).
* **Design Patterns appliqués :** Utilisation de l'héritage, du polymorphisme et du pattern *Composite* pour enchaîner dynamiquement des filtres multi-critères.
* **Pipeline de traitement :** Validation de structure, normalisation $\log_2$, et génération de rendus interactifs (Barplot, Heatmap, Volcano Plot).
