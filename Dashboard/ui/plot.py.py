"""
===============================================================================
Projet : Dashboard Dash Omique (POO)
Auteur : Kpaka Mouhamadou Adesanya
Module : ui/plots.py
Description : Classes de génération des figures Plotly (Barplot, Heatmap, Volcano).
===============================================================================
"""

import pandas as pd
import numpy as np
import plotly.express as px


class BasePlot:
    """
    Classe abstraite de base pour la génération de graphiques Plotly.
    """
    def __init__(self, data: pd.DataFrame, title=""):
        self.data = data
        self.title = title
        self.figure = None

    def build(self):
        """Méthode abstraite construisant l'objet Figure."""
        raise NotImplementedError("La méthode build() doit être implémentée dans la sous-classe.")

    def get_figure(self):
        """
        Renvoie la figure Plotly, en la construisant si elle n'est pas encore instanciée.
        """
        if self.figure is None:
            self.build()
        return self.figure


class BarPlot(BasePlot):
    """
    Génère un diagramme en barres groupées (Expression par gène et par condition).
    """
    def build(self):
        if self.data is None or self.data.empty:
            self.figure = px.bar(title="Aucune donnée disponible.")
            return
            
        self.figure = px.bar(
            self.data, 
            x="gene", 
            y="expression_norm",
            color="condition", 
            title=self.title,
            barmode="group", 
            color_discrete_sequence=['#3bc9db', '#ff8787']
        )
        self.figure.update_layout(plot_bgcolor='white', paper_bgcolor='white')


class HeatmapPlot(BasePlot):
    """
    Génère une carte thermique (Heatmap) d'expression génique par condition.
    """
    def build(self):
        if self.data is None or self.data.empty:
            self.figure = px.imshow([[0]], title="Aucune donnée disponible.")
            return
        
        # Agrégation moyenne pour gérer les éventuels réplicats
        agg_data = self.data.groupby(['gene', 'condition'])['expression_norm'].mean().reset_index()
        pivot = agg_data.pivot(index="gene", columns="condition", values="expression_norm")
        
        self.figure = px.imshow(
            pivot, 
            title=self.title,
            color_continuous_scale="RdBu_r", 
            aspect="auto"
        )


class VolcanoPlot(BasePlot):
    """
    Génère un Volcano Plot (Significativité statistique vs Amplitude de variation).
    """
    def build(self):
        if self.data is None or self.data.empty:
            self.figure = px.scatter(title="Aucune donnée disponible.")
            return
            
        # Simulation statistique si les colonnes spécifiques sont absentes
        if "p_value" not in self.data.columns or "fold_change" not in self.data.columns:
            df_volcano = self.data.copy()
            np.random.seed(42)
            df_volcano["p_value"] = np.random.uniform(0.0001, 0.1, size=len(df_volcano))
            df_volcano["fold_change"] = np.random.normal(0, 2, size=len(df_volcano))
            df_volcano["significant"] = df_volcano["p_value"] < 0.05
        else:
            df_volcano = self.data

        df_volcano["-log10(p)"] = -np.log10(df_volcano["p_value"] + 1e-10)
        self.figure = px.scatter(
            df_volcano, 
            x="fold_change", 
            y="-log10(p)",
            color="significant", 
            hover_name="gene",
            title=self.title, 
            color_discrete_map={True: '#e03131', False: '#ced4da'}
        )
        self.figure.update_layout(plot_bgcolor='white', paper_bgcolor='white')